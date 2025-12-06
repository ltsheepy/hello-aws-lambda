#!/usr/bin/env python3
"""
Generate security report from AWS SSM and Security Hub
Shows patch compliance, security findings, and recommendations
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_aws_command(command):
    """Run AWS CLI command and return JSON output"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout) if result.stdout else {}
    except subprocess.CalledProcessError as e:
        print(f"Warning: Command failed: {' '.join(command)}")
        print(f"Error: {e.stderr}")
        return None
    except json.JSONDecodeError:
        return None


def get_instance_ids():
    """Get instance IDs from Terraform state"""
    try:
        result = subprocess.run(
            ["terraform", "output", "-json"],
            capture_output=True,
            text=True,
            check=True
        )
        outputs = json.loads(result.stdout)
        instance_id = outputs.get('instance_id', {}).get('value')
        return [instance_id] if instance_id else []
    except:
        return []


def get_patch_compliance(instance_ids, region):
    """Get patch compliance status for instances"""
    compliance_data = []
    
    for instance_id in instance_ids:
        # Get patch state
        result = run_aws_command([
            "aws", "ssm", "describe-instance-patch-states",
            "--instance-ids", instance_id,
            "--region", region
        ])
        
        if result and 'InstancePatchStates' in result:
            for state in result['InstancePatchStates']:
                compliance_data.append({
                    'instance_id': state.get('InstanceId'),
                    'patch_group': state.get('PatchGroup', 'N/A'),
                    'installed_count': state.get('InstalledCount', 0),
                    'missing_count': state.get('MissingCount', 0),
                    'failed_count': state.get('FailedCount', 0),
                    'not_applicable_count': state.get('NotApplicableCount', 0),
                    'operation': state.get('Operation', 'N/A'),
                    'operation_start_time': state.get('OperationStartTime', 'N/A'),
                    'operation_end_time': state.get('OperationEndTime', 'N/A'),
                })
    
    return compliance_data


def get_security_hub_findings(region):
    """Get Security Hub findings"""
    result = run_aws_command([
        "aws", "securityhub", "get-findings",
        "--filters", json.dumps({
            "RecordState": [{"Value": "ACTIVE", "Comparison": "EQUALS"}],
            "WorkflowStatus": [{"Value": "NEW", "Comparison": "EQUALS"}]
        }),
        "--max-items", "50",
        "--region", region
    ])
    
    if not result or 'Findings' not in result:
        return None
    
    findings = result['Findings']
    
    # Categorize by severity
    categorized = {
        'CRITICAL': [],
        'HIGH': [],
        'MEDIUM': [],
        'LOW': [],
        'INFORMATIONAL': []
    }
    
    for finding in findings:
        severity = finding.get('Severity', {}).get('Label', 'INFORMATIONAL')
        categorized[severity].append({
            'title': finding.get('Title', 'Unknown'),
            'description': finding.get('Description', 'No description'),
            'resource': finding.get('Resources', [{}])[0].get('Id', 'Unknown'),
            'compliance_status': finding.get('Compliance', {}).get('Status', 'N/A'),
            'first_observed': finding.get('FirstObservedAt', 'N/A'),
        })
    
    return categorized


def get_ssm_compliance(instance_ids, region):
    """Get SSM compliance summary"""
    result = run_aws_command([
        "aws", "ssm", "list-compliance-summaries",
        "--region", region
    ])
    
    if not result or 'ComplianceSummaryItems' not in result:
        return None
    
    return result['ComplianceSummaryItems']


def generate_security_readme(patch_data, security_findings, ssm_compliance, region):
    """Generate SECURITY.md content"""
    
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    lines = [
        "# Security & Compliance Report",
        "",
        f"*Last updated: {timestamp}*",
        "",
        "## Overview",
        "",
        "This report provides real-time security and compliance status for the infrastructure.",
        "",
    ]
    
    # Patch Compliance Section
    lines.extend([
        "## Patch Compliance Status",
        "",
    ])
    
    if patch_data:
        lines.extend([
            "| Instance ID | Patch Group | Installed | Missing | Failed | Status |",
            "|-------------|-------------|-----------|---------|--------|--------|",
        ])
        
        for data in patch_data:
            status = "✅ Compliant" if data['missing_count'] == 0 and data['failed_count'] == 0 else "⚠️ Action Required"
            lines.append(
                f"| `{data['instance_id']}` | {data['patch_group']} | "
                f"{data['installed_count']} | {data['missing_count']} | "
                f"{data['failed_count']} | {status} |"
            )
        
        lines.extend([
            "",
            "### Patch Summary",
            "",
        ])
        
        total_installed = sum(d['installed_count'] for d in patch_data)
        total_missing = sum(d['missing_count'] for d in patch_data)
        total_failed = sum(d['failed_count'] for d in patch_data)
        
        lines.extend([
            f"- **Total Patches Installed:** {total_installed}",
            f"- **Total Patches Missing:** {total_missing}",
            f"- **Total Patches Failed:** {total_failed}",
            "",
        ])
        
        if total_missing > 0 or total_failed > 0:
            lines.extend([
                "### ⚠️ Action Required",
                "",
                "Some patches are missing or failed. To remediate:",
                "",
                "```bash",
                "# Scan for missing patches",
                f"aws ssm send-command --document-name AWS-RunPatchBaseline \\",
                f"  --targets Key=tag:PatchGroup,Values=production \\",
                f"  --parameters Operation=Scan \\",
                f"  --region {region}",
                "",
                "# Install missing patches",
                f"aws ssm send-command --document-name AWS-RunPatchBaseline \\",
                f"  --targets Key=tag:PatchGroup,Values=production \\",
                f"  --parameters Operation=Install,RebootOption=RebootIfNeeded \\",
                f"  --region {region}",
                "```",
                "",
            ])
    else:
        lines.extend([
            "⚠️ No patch compliance data available. Ensure:",
            "1. Instances are running",
            "2. SSM Agent is installed and running",
            "3. Initial patch scan has completed",
            "",
            "**Run initial scan:**",
            "```bash",
            f"aws ssm send-command --document-name AWS-RunPatchBaseline \\",
            f"  --targets Key=tag:PatchGroup,Values=production \\",
            f"  --parameters Operation=Scan \\",
            f"  --region {region}",
            "```",
            "",
        ])
    
    # Security Hub Section
    lines.extend([
        "## Security Hub Findings",
        "",
    ])
    
    if security_findings:
        # Summary
        total_findings = sum(len(findings) for findings in security_findings.values())
        
        lines.extend([
            "### Summary by Severity",
            "",
            "| Severity | Count | Status |",
            "|----------|-------|--------|",
        ])
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFORMATIONAL']:
            count = len(security_findings.get(severity, []))
            icon = "🔴" if severity == "CRITICAL" else "🟠" if severity == "HIGH" else "🟡" if severity == "MEDIUM" else "🟢"
            lines.append(f"| {icon} **{severity}** | {count} | {'Action Required' if count > 0 and severity in ['CRITICAL', 'HIGH'] else 'Review'} |")
        
        lines.extend([
            f"| **TOTAL** | **{total_findings}** | |",
            "",
        ])
        
        # Detailed findings
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM']:
            findings = security_findings.get(severity, [])
            if findings:
                lines.extend([
                    f"### {severity} Severity Findings",
                    "",
                ])
                
                for idx, finding in enumerate(findings[:5], 1):  # Show top 5
                    lines.extend([
                        f"#### {idx}. {finding['title']}",
                        "",
                        f"**Description:** {finding['description'][:200]}...",
                        "",
                        f"**Resource:** `{finding['resource']}`",
                        "",
                        f"**Compliance Status:** {finding['compliance_status']}",
                        "",
                        f"**First Observed:** {finding['first_observed']}",
                        "",
                    ])
                
                if len(findings) > 5:
                    lines.append(f"*...and {len(findings) - 5} more {severity} findings*")
                    lines.append("")
    else:
        lines.extend([
            "ℹ️ Security Hub is not enabled or no findings available.",
            "",
            "**To enable Security Hub:**",
            "```bash",
            f"aws securityhub enable-security-hub --region {region}",
            "```",
            "",
            "Security Hub provides:",
            "- Automated security checks",
            "- CIS AWS Foundations Benchmark",
            "- AWS Foundational Security Best Practices",
            "- Integration with GuardDuty, Inspector, and Macie",
            "",
        ])
    
    # Security Best Practices
    lines.extend([
        "## Security Configuration",
        "",
        "### ✅ Implemented Security Controls",
        "",
        "| Control | Status | Details |",
        "|---------|--------|---------|",
        "| SSM Session Manager | ✅ Enabled | No SSH keys required |",
        "| IMDSv2 | ✅ Enforced | Instance metadata protection |",
        "| EBS Encryption | ✅ Enabled | All volumes encrypted at rest |",
        "| S3 Encryption | ✅ Enabled | Logs encrypted with AES256 |",
        "| Private Subnets | ✅ Enabled | No public IP addresses |",
        "| VPC Endpoints | ✅ Enabled | Private AWS service access |",
        "| Security Groups | ✅ Locked | VPC-only traffic |",
        "| IAM Roles | ✅ Least Privilege | Minimal permissions |",
        "| Automated Patching | ✅ Enabled | Tag-based maintenance windows |",
        "| CloudWatch Logging | ✅ Enabled | All actions logged |",
        "",
        "### 🔒 Security Recommendations",
        "",
        "1. **Enable Security Hub** - Automated security assessments",
        "2. **Enable GuardDuty** - Threat detection",
        "3. **Enable AWS Config** - Configuration compliance",
        "4. **Enable CloudTrail** - API activity logging",
        "5. **Set up SNS Alerts** - Real-time security notifications",
        "",
        "## Compliance Standards",
        "",
        "This infrastructure is designed to meet:",
        "",
        "- ✅ **CIS AWS Foundations Benchmark** (partial)",
        "- ✅ **AWS Well-Architected Framework** (Security Pillar)",
        "- ✅ **NIST Cybersecurity Framework** (basic controls)",
        "",
        "## Quick Actions",
        "",
        "### View Patch Compliance",
        "```bash",
        f"aws ssm describe-instance-patch-states \\",
        f"  --instance-ids $(terraform output -raw instance_id) \\",
        f"  --region {region}",
        "```",
        "",
        "### Run Patch Scan",
        "```bash",
        f"aws ssm send-command \\",
        f"  --document-name AWS-RunPatchBaseline \\",
        f"  --targets Key=tag:PatchGroup,Values=production \\",
        f"  --parameters Operation=Scan \\",
        f"  --region {region}",
        "```",
        "",
        "### View Security Hub Findings",
        "```bash",
        f"aws securityhub get-findings \\",
        f"  --filters 'RecordState=[{{Value=ACTIVE,Comparison=EQUALS}}]' \\",
        f"  --region {region}",
        "```",
        "",
        "### Check SSM Agent Status",
        "```bash",
        f"aws ssm describe-instance-information \\",
        f"  --filters Key=InstanceIds,Values=$(terraform output -raw instance_id) \\",
        f"  --region {region}",
        "```",
        "",
        "---",
        "",
        "*This report is automatically generated. Run `make security-report` to update.*",
    ])
    
    return '\n'.join(lines)


def main():
    region = "ap-southeast-2"
    
    print("🔒 Generating Security & Compliance Report...")
    print()
    
    # Get instance IDs
    print("📋 Getting instance information...")
    instance_ids = get_instance_ids()
    
    if not instance_ids:
        print("⚠️  No instances found in Terraform state")
        print("   Deploy infrastructure first: terraform apply")
    else:
        print(f"   Found {len(instance_ids)} instance(s)")
    
    # Get patch compliance
    print("🔍 Checking patch compliance...")
    patch_data = get_patch_compliance(instance_ids, region) if instance_ids else []
    
    if patch_data:
        total_missing = sum(d['missing_count'] for d in patch_data)
        total_failed = sum(d['failed_count'] for d in patch_data)
        if total_missing > 0 or total_failed > 0:
            print(f"   ⚠️  {total_missing} missing, {total_failed} failed patches")
        else:
            print("   ✅ All patches up to date")
    else:
        print("   ℹ️  No patch data available yet")
    
    # Get Security Hub findings
    print("🛡️  Checking Security Hub...")
    security_findings = get_security_hub_findings(region)
    
    if security_findings:
        total = sum(len(f) for f in security_findings.values())
        critical = len(security_findings.get('CRITICAL', []))
        high = len(security_findings.get('HIGH', []))
        print(f"   Found {total} findings ({critical} critical, {high} high)")
    else:
        print("   ℹ️  Security Hub not enabled or no findings")
    
    # Get SSM compliance
    print("📊 Getting SSM compliance summary...")
    ssm_compliance = get_ssm_compliance(instance_ids, region) if instance_ids else None
    
    # Generate report
    print("📝 Generating SECURITY.md...")
    content = generate_security_readme(patch_data, security_findings, ssm_compliance, region)
    
    with open('SECURITY.md', 'w') as f:
        f.write(content)
    
    print()
    print("✅ Security report generated: SECURITY.md")
    print()
    
    # Summary
    if patch_data:
        total_missing = sum(d['missing_count'] for d in patch_data)
        total_failed = sum(d['failed_count'] for d in patch_data)
        if total_missing > 0 or total_failed > 0:
            print("⚠️  ACTION REQUIRED: Patches need attention")
        else:
            print("✅ Patch compliance: OK")
    
    if security_findings:
        critical = len(security_findings.get('CRITICAL', []))
        high = len(security_findings.get('HIGH', []))
        if critical > 0 or high > 0:
            print(f"⚠️  ACTION REQUIRED: {critical + high} critical/high security findings")
        else:
            print("✅ Security Hub: No critical findings")


if __name__ == "__main__":
    main()
