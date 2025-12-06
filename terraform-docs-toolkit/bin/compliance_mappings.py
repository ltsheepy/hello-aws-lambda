"""
Compliance framework mappings for security findings
Maps AWS Security Hub findings to:
- AWS Well-Architected Framework (WAF)
- CIS Controls v8
- NIST 800-53 Rev 5
"""

# Common Security Hub finding types mapped to frameworks
COMPLIANCE_MAPPINGS = {
    # IAM Findings
    'IAM.1': {
        'title': 'IAM policies should not allow full "*:*" administrative privileges',
        'waf': ['SEC-02: Identity and Access Management'],
        'cis_v8': ['5.4: Restrict Administrator Privileges to Dedicated Administrator Accounts'],
        'nist_800_53': ['AC-6: Least Privilege', 'AC-2: Account Management']
    },
    'IAM.2': {
        'title': 'IAM users should not have IAM policies attached',
        'waf': ['SEC-02: Identity and Access Management'],
        'cis_v8': ['5.2: Use Unique Passwords', '6.1: Establish an Access Granting Process'],
        'nist_800_53': ['AC-2: Account Management', 'IA-2: Identification and Authentication']
    },
    'IAM.3': {
        'title': 'IAM users access keys should be rotated every 90 days or less',
        'waf': ['SEC-02: Identity and Access Management'],
        'cis_v8': ['5.2: Use Unique Passwords'],
        'nist_800_53': ['IA-5: Authenticator Management']
    },
    'IAM.4': {
        'title': 'IAM root user access key should not exist',
        'waf': ['SEC-02: Identity and Access Management'],
        'cis_v8': ['5.4: Restrict Administrator Privileges to Dedicated Administrator Accounts'],
        'nist_800_53': ['AC-6: Least Privilege', 'IA-2: Identification and Authentication']
    },
    'IAM.5': {
        'title': 'MFA should be enabled for all IAM users',
        'waf': ['SEC-02: Identity and Access Management'],
        'cis_v8': ['6.3: Require MFA for Externally-Exposed Applications'],
        'nist_800_53': ['IA-2(1): Multi-Factor Authentication']
    },
    'IAM.6': {
        'title': 'Hardware MFA should be enabled for the root user',
        'waf': ['SEC-02: Identity and Access Management'],
        'cis_v8': ['6.3: Require MFA for Externally-Exposed Applications'],
        'nist_800_53': ['IA-2(1): Multi-Factor Authentication', 'IA-2(11): Remote Access']
    },
    
    # EC2 Findings
    'EC2.1': {
        'title': 'Amazon EBS snapshots should not be publicly restorable',
        'waf': ['SEC-03: Detective Controls', 'SEC-05: Data Protection'],
        'cis_v8': ['3.3: Configure Data Access Control Lists'],
        'nist_800_53': ['AC-3: Access Enforcement', 'SC-28: Protection of Information at Rest']
    },
    'EC2.2': {
        'title': 'VPC default security group should not allow inbound and outbound traffic',
        'waf': ['SEC-05: Infrastructure Protection'],
        'cis_v8': ['12.3: Securely Manage Network Infrastructure'],
        'nist_800_53': ['SC-7: Boundary Protection', 'AC-4: Information Flow Enforcement']
    },
    'EC2.3': {
        'title': 'Attached EBS volumes should be encrypted at rest',
        'waf': ['SEC-08: Data Protection'],
        'cis_v8': ['3.11: Encrypt Sensitive Data at Rest'],
        'nist_800_53': ['SC-28: Protection of Information at Rest', 'SC-28(1): Cryptographic Protection']
    },
    'EC2.6': {
        'title': 'VPC flow logging should be enabled in all VPCs',
        'waf': ['SEC-04: Detection'],
        'cis_v8': ['8.2: Collect Audit Logs', '8.5: Collect Detailed Audit Logs'],
        'nist_800_53': ['AU-2: Audit Events', 'AU-12: Audit Generation', 'SI-4: System Monitoring']
    },
    'EC2.7': {
        'title': 'EBS default encryption should be enabled',
        'waf': ['SEC-08: Data Protection'],
        'cis_v8': ['3.11: Encrypt Sensitive Data at Rest'],
        'nist_800_53': ['SC-28: Protection of Information at Rest']
    },
    'EC2.8': {
        'title': 'EC2 instances should use IMDSv2',
        'waf': ['SEC-05: Infrastructure Protection'],
        'cis_v8': ['4.1: Establish and Maintain a Secure Configuration Process'],
        'nist_800_53': ['CM-6: Configuration Settings', 'SC-8: Transmission Confidentiality']
    },
    'EC2.10': {
        'title': 'Amazon EC2 should be configured to use VPC endpoints',
        'waf': ['SEC-05: Infrastructure Protection'],
        'cis_v8': ['12.3: Securely Manage Network Infrastructure'],
        'nist_800_53': ['SC-7: Boundary Protection']
    },
    
    # S3 Findings
    'S3.1': {
        'title': 'S3 Block Public Access setting should be enabled',
        'waf': ['SEC-05: Data Protection'],
        'cis_v8': ['3.3: Configure Data Access Control Lists'],
        'nist_800_53': ['AC-3: Access Enforcement', 'AC-6: Least Privilege']
    },
    'S3.2': {
        'title': 'S3 buckets should prohibit public read access',
        'waf': ['SEC-05: Data Protection'],
        'cis_v8': ['3.3: Configure Data Access Control Lists'],
        'nist_800_53': ['AC-3: Access Enforcement']
    },
    'S3.3': {
        'title': 'S3 buckets should prohibit public write access',
        'waf': ['SEC-05: Data Protection'],
        'cis_v8': ['3.3: Configure Data Access Control Lists'],
        'nist_800_53': ['AC-3: Access Enforcement']
    },
    'S3.4': {
        'title': 'S3 buckets should have server-side encryption enabled',
        'waf': ['SEC-08: Data Protection'],
        'cis_v8': ['3.11: Encrypt Sensitive Data at Rest'],
        'nist_800_53': ['SC-28: Protection of Information at Rest']
    },
    'S3.5': {
        'title': 'S3 buckets should require requests to use SSL',
        'waf': ['SEC-08: Data Protection'],
        'cis_v8': ['3.10: Encrypt Sensitive Data in Transit'],
        'nist_800_53': ['SC-8: Transmission Confidentiality', 'SC-13: Cryptographic Protection']
    },
    'S3.8': {
        'title': 'S3 Block Public Access setting should be enabled at the bucket level',
        'waf': ['SEC-05: Data Protection'],
        'cis_v8': ['3.3: Configure Data Access Control Lists'],
        'nist_800_53': ['AC-3: Access Enforcement']
    },
    
    # CloudTrail Findings
    'CloudTrail.1': {
        'title': 'CloudTrail should be enabled and configured with at least one multi-Region trail',
        'waf': ['SEC-04: Detection'],
        'cis_v8': ['8.2: Collect Audit Logs', '8.5: Collect Detailed Audit Logs'],
        'nist_800_53': ['AU-2: Audit Events', 'AU-3: Content of Audit Records', 'AU-12: Audit Generation']
    },
    'CloudTrail.2': {
        'title': 'CloudTrail should have encryption at rest enabled',
        'waf': ['SEC-08: Data Protection'],
        'cis_v8': ['3.11: Encrypt Sensitive Data at Rest'],
        'nist_800_53': ['SC-28: Protection of Information at Rest']
    },
    'CloudTrail.4': {
        'title': 'CloudTrail log file validation should be enabled',
        'waf': ['SEC-04: Detection'],
        'cis_v8': ['8.3: Ensure Adequate Audit Log Storage'],
        'nist_800_53': ['AU-9: Protection of Audit Information']
    },
    
    # Config Findings
    'Config.1': {
        'title': 'AWS Config should be enabled',
        'waf': ['SEC-04: Detection'],
        'cis_v8': ['8.2: Collect Audit Logs'],
        'nist_800_53': ['CM-3: Configuration Change Control', 'CM-8: System Component Inventory']
    },
    
    # GuardDuty Findings
    'GuardDuty.1': {
        'title': 'GuardDuty should be enabled',
        'waf': ['SEC-04: Detection'],
        'cis_v8': ['8.11: Conduct Audit Log Reviews'],
        'nist_800_53': ['SI-4: System Monitoring', 'IR-4: Incident Handling']
    },
    
    # SecurityHub Findings
    'SecurityHub.1': {
        'title': 'Security Hub should be enabled',
        'waf': ['SEC-01: Security Foundations', 'SEC-04: Detection'],
        'cis_v8': ['17.1: Designate Personnel to Manage Incident Handling'],
        'nist_800_53': ['SI-4: System Monitoring', 'RA-5: Vulnerability Monitoring']
    },
    
    # SSM Findings
    'SSM.1': {
        'title': 'EC2 instances should be managed by AWS Systems Manager',
        'waf': ['OPS-05: Patch Management'],
        'cis_v8': ['7.1: Establish and Maintain a Vulnerability Management Process'],
        'nist_800_53': ['SI-2: Flaw Remediation', 'CM-3: Configuration Change Control']
    },
    'SSM.2': {
        'title': 'All EC2 instances managed by Systems Manager should be compliant with patching requirements',
        'waf': ['OPS-05: Patch Management'],
        'cis_v8': ['7.2: Establish and Maintain a Remediation Process', '7.3: Perform Automated Operating System Patch Management'],
        'nist_800_53': ['SI-2: Flaw Remediation', 'SI-2(2): Automated Flaw Remediation Status']
    },
    'SSM.3': {
        'title': 'Instances managed by Systems Manager should have an association compliance status of COMPLIANT',
        'waf': ['OPS-05: Patch Management'],
        'cis_v8': ['7.3: Perform Automated Operating System Patch Management'],
        'nist_800_53': ['SI-2: Flaw Remediation', 'CM-2: Baseline Configuration']
    },
}


def get_compliance_mapping(finding_id):
    """Get compliance framework mappings for a finding ID"""
    # Extract the base finding ID (e.g., "IAM.1" from "arn:aws:securityhub:...:IAM.1")
    if '/' in finding_id:
        finding_id = finding_id.split('/')[-1]
    
    # Try exact match first
    if finding_id in COMPLIANCE_MAPPINGS:
        return COMPLIANCE_MAPPINGS[finding_id]
    
    # Try prefix match (e.g., "IAM" from "IAM.1")
    prefix = finding_id.split('.')[0] if '.' in finding_id else finding_id
    
    # Return generic mapping based on category
    generic_mappings = {
        'IAM': {
            'waf': ['SEC-02: Identity and Access Management'],
            'cis_v8': ['5: Account Management', '6: Access Control Management'],
            'nist_800_53': ['AC-2: Account Management', 'IA-2: Identification and Authentication']
        },
        'EC2': {
            'waf': ['SEC-05: Infrastructure Protection'],
            'cis_v8': ['4: Secure Configuration', '12: Network Infrastructure Management'],
            'nist_800_53': ['CM-6: Configuration Settings', 'SC-7: Boundary Protection']
        },
        'S3': {
            'waf': ['SEC-08: Data Protection'],
            'cis_v8': ['3: Data Protection', '13: Data Security'],
            'nist_800_53': ['SC-28: Protection of Information at Rest', 'AC-3: Access Enforcement']
        },
        'CloudTrail': {
            'waf': ['SEC-04: Detection'],
            'cis_v8': ['8: Audit Log Management'],
            'nist_800_53': ['AU-2: Audit Events', 'AU-12: Audit Generation']
        },
        'SSM': {
            'waf': ['OPS-05: Patch Management'],
            'cis_v8': ['7: Continuous Vulnerability Management'],
            'nist_800_53': ['SI-2: Flaw Remediation', 'CM-3: Configuration Change Control']
        },
    }
    
    return generic_mappings.get(prefix, {
        'waf': ['SEC-01: Security Foundations'],
        'cis_v8': ['General Security Controls'],
        'nist_800_53': ['General Security Controls']
    })


def format_compliance_badges(mapping):
    """Format compliance mappings as markdown badges"""
    lines = []
    
    if mapping.get('waf'):
        lines.append("**AWS WAF:** " + " | ".join(f"`{w}`" for w in mapping['waf']))
    
    if mapping.get('cis_v8'):
        lines.append("**CIS v8:** " + " | ".join(f"`{c}`" for c in mapping['cis_v8']))
    
    if mapping.get('nist_800_53'):
        lines.append("**NIST 800-53:** " + " | ".join(f"`{n}`" for n in mapping['nist_800_53']))
    
    return lines
