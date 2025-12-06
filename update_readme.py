#!/usr/bin/env python3
"""
Update README.md with current infrastructure details
Includes diagram, costs, and resource inventory
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path


# AWS Pricing (Sydney region - ap-southeast-2)
PRICING = {
    't3.micro': {'hourly': 0.015, 'monthly': 10.95},
    't3.small': {'hourly': 0.030, 'monthly': 21.90},
    't3.medium': {'hourly': 0.060, 'monthly': 43.80},
    't2.micro': {'hourly': 0.017, 'monthly': 12.41},
    'ebs_gp3_gb': 0.096,  # per GB per month
    'vpc_endpoint': 0.01,  # per hour
    'vpc_endpoint_data': 0.01,  # per GB
    'nat_gateway': 0.066,  # per hour
    'nat_gateway_data': 0.059,  # per GB
    's3_storage': 0.025,  # per GB per month
    's3_requests': 0.005,  # per 1000 requests
    'cloudwatch_logs_ingestion': 0.50,  # per GB
    'cloudwatch_logs_storage': 0.03,  # per GB per month
}


def load_metadata():
    """Load architecture metadata"""
    try:
        with open('architecture-metadata.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: architecture-metadata.json not found. Run 'make diagram' first.")
        return None


def get_terraform_outputs():
    """Get Terraform outputs"""
    try:
        result = subprocess.run(
            ["terraform", "output", "-json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except:
        return {}


def calculate_costs(metadata):
    """Calculate monthly costs based on resources"""
    costs = {
        'compute': [],
        'storage': [],
        'networking': [],
        'monitoring': [],
        'free_services': [],
    }
    
    total = 0.0
    
    # EC2 Instances - individual breakdown
    for idx, instance in enumerate(metadata['resources'].get('instance_details', [])):
        instance_type = instance.get('type', 't3.micro')
        instance_name = instance.get('name', f'Instance-{idx+1}')
        cost = PRICING.get(instance_type, PRICING['t3.micro'])['monthly']
        costs['compute'].append({
            'item': f"EC2 Instance: {instance_name}",
            'details': f"{instance_type} (730 hrs/month)",
            'cost': cost
        })
        total += cost
    
    # EBS Volumes - individual per instance
    for idx, instance in enumerate(metadata['resources'].get('instance_details', [])):
        instance_name = instance.get('name', f'Instance-{idx+1}')
        ebs_cost = 30 * PRICING['ebs_gp3_gb']
        costs['storage'].append({
            'item': f"EBS Volume: {instance_name}",
            'details': "30GB gp3 encrypted",
            'cost': ebs_cost
        })
        total += ebs_cost
    
    # VPC Endpoints - individual breakdown
    endpoints = metadata.get('endpoints', [])
    for endpoint in endpoints:
        if endpoint.lower() == 's3':
            # S3 Gateway endpoint is free
            costs['free_services'].append({
                'item': f"VPC Endpoint: {endpoint.upper()}",
                'details': "Gateway endpoint (FREE)",
                'cost': 0.0
            })
        else:
            # Interface endpoints cost money
            endpoint_cost = PRICING['vpc_endpoint'] * 730
            costs['networking'].append({
                'item': f"VPC Endpoint: {endpoint.upper()}",
                'details': "Interface endpoint (730 hrs)",
                'cost': endpoint_cost
            })
            total += endpoint_cost
    
    # Endpoint data transfer (estimate per endpoint)
    interface_endpoints = [e for e in endpoints if e.lower() != 's3']
    if interface_endpoints:
        data_per_endpoint = 5 / len(interface_endpoints) if interface_endpoints else 0
        for endpoint in interface_endpoints:
            data_cost = data_per_endpoint * PRICING['vpc_endpoint_data']
            costs['networking'].append({
                'item': f"VPC Endpoint Data: {endpoint.upper()}",
                'details': f"~{data_per_endpoint:.1f}GB/month",
                'cost': data_cost
            })
            total += data_cost
    
    # NAT Gateway
    if metadata['resources'].get('has_nat_gateway'):
        nat_cost = PRICING['nat_gateway'] * 730
        costs['networking'].append({
            'item': "NAT Gateway",
            'details': "730 hours/month",
            'cost': nat_cost
        })
        total += nat_cost
        
        nat_data_cost = 10 * PRICING['nat_gateway_data']
        costs['networking'].append({
            'item': "NAT Gateway Data",
            'details': "~10GB/month",
            'cost': nat_data_cost
        })
        total += nat_data_cost
    
    # S3 Storage - per bucket
    num_buckets = metadata['resources'].get('s3_buckets', 0)
    if num_buckets > 0:
        storage_per_bucket = 1.0 / num_buckets  # Distribute 1GB across buckets
        for i in range(num_buckets):
            s3_cost = storage_per_bucket * PRICING['s3_storage']
            costs['storage'].append({
                'item': f"S3 Bucket {i+1}: Storage",
                'details': f"~{storage_per_bucket:.1f}GB logs",
                'cost': s3_cost
            })
            total += s3_cost
        
        # S3 Requests
        requests_per_bucket = 10 / num_buckets
        for i in range(num_buckets):
            s3_requests_cost = requests_per_bucket * PRICING['s3_requests']
            costs['storage'].append({
                'item': f"S3 Bucket {i+1}: Requests",
                'details': f"~{requests_per_bucket:.0f}k PUT/GET",
                'cost': s3_requests_cost
            })
            total += s3_requests_cost
    
    # CloudWatch Logs - per log group
    num_mw = metadata['resources'].get('maintenance_windows', 0)
    if num_mw > 0:
        ingestion_per_mw = 0.5 / num_mw
        storage_per_mw = 1.0 / num_mw
        
        for i in range(num_mw):
            cw_ingestion = ingestion_per_mw * PRICING['cloudwatch_logs_ingestion']
            costs['monitoring'].append({
                'item': f"CloudWatch Logs {i+1}: Ingestion",
                'details': f"~{ingestion_per_mw*1000:.0f}MB",
                'cost': cw_ingestion
            })
            total += cw_ingestion
            
            cw_storage = storage_per_mw * PRICING['cloudwatch_logs_storage']
            costs['monitoring'].append({
                'item': f"CloudWatch Logs {i+1}: Storage",
                'details': f"~{storage_per_mw*1000:.0f}MB",
                'cost': cw_storage
            })
            total += cw_storage
    
    # Free AWS Services
    costs['free_services'].extend([
        {'item': 'SSM Session Manager', 'details': 'Unlimited sessions', 'cost': 0.0},
        {'item': 'SSM Patch Manager', 'details': 'Unlimited patches', 'cost': 0.0},
        {'item': 'SSM Inventory', 'details': 'Unlimited collection', 'cost': 0.0},
        {'item': 'SSM Maintenance Windows', 'details': f"{num_mw} windows", 'cost': 0.0},
    ])
    
    return costs, total


def generate_cost_table(costs, total):
    """Generate detailed markdown cost table"""
    lines = []
    
    # Summary table first
    lines.append("### Cost Summary by Category")
    lines.append("")
    lines.append("| Category | Monthly Cost | % of Total |")
    lines.append("|----------|--------------|------------|")
    
    category_totals = {}
    for category, items in costs.items():
        if category == 'free_services':
            continue
        if items:
            category_total = sum(item['cost'] for item in items)
            category_totals[category] = category_total
            percentage = (category_total / total * 100) if total > 0 else 0
            lines.append(f"| **{category.title()}** | ${category_total:.2f} | {percentage:.1f}% |")
    
    lines.append(f"| **TOTAL** | **${total:.2f}** | **100%** |")
    
    # Detailed breakdown by category
    lines.append("")
    lines.append("### Detailed Cost Breakdown")
    lines.append("")
    lines.append("| Category | Resource | Details | Hourly | Monthly | Annual |")
    lines.append("|----------|----------|---------|--------|---------|--------|")
    
    for category, items in costs.items():
        if not items or category == 'free_services':
            continue
        
        for idx, item in enumerate(items):
            hourly = item['cost'] / 730  # Approximate hours per month
            annual = item['cost'] * 12
            
            # Show category name only on first row
            category_display = f"**{category.title()}**" if idx == 0 else ""
            
            lines.append(
                f"| {category_display} | {item['item']} | {item['details']} | "
                f"${hourly:.4f} | ${item['cost']:.2f} | ${annual:.2f} |"
            )
    
    lines.append(f"| | **TOTAL** | | | **${total:.2f}** | **${total * 12:.2f}** |")
    
    return '\n'.join(lines)


def generate_resource_table(metadata):
    """Generate resource inventory table"""
    resources = metadata['resources']
    
    lines = [
        "| Resource Type | Count | Details |",
        "|---------------|-------|---------|",
        f"| VPC | 1 | {resources.get('vpc_cidr', 'N/A')} |",
        f"| Subnets | {resources.get('subnets', 0)} | Private only |",
        f"| EC2 Instances | {resources.get('instances', 0)} | See details below |",
        f"| VPC Endpoints | {resources.get('vpc_endpoints', 0)} | {', '.join(metadata.get('endpoints', [])[:3])} |",
        f"| Maintenance Windows | {resources.get('maintenance_windows', 0)} | Tag-based patching |",
        f"| S3 Buckets | {resources.get('s3_buckets', 0)} | Encrypted logs |",
        f"| NAT Gateway | {'Yes' if resources.get('has_nat_gateway') else 'No'} | {'$48/month' if resources.get('has_nat_gateway') else 'Cost savings'} |",
        f"| Internet Gateway | {'Yes' if resources.get('has_internet_gateway') else 'No'} | {'Public access' if resources.get('has_internet_gateway') else 'Private only'} |",
    ]
    
    if metadata['resources'].get('instance_details'):
        lines.append("")
        lines.append("### EC2 Instance Details")
        lines.append("| Name | Type | Patch Group |")
        lines.append("|------|------|-------------|")
        for inst in metadata['resources']['instance_details']:
            lines.append(f"| {inst['name']} | {inst['type']} | {inst['patch_group']} |")
    
    return '\n'.join(lines)


def update_readme(metadata, costs, total):
    """Update README.md with current data"""
    
    # Read current README
    readme_path = Path('README.md')
    if not readme_path.exists():
        print("Error: README.md not found")
        return False
    
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Generate sections
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    architecture_section = f"""## Architecture

![Architecture Diagram](architecture.png)

*Last updated: {timestamp}*

### Infrastructure Overview

{generate_resource_table(metadata)}
"""
    
    cost_section = f"""## Cost Breakdown

*Estimated monthly costs for Sydney (ap-southeast-2) region*

{generate_cost_table(costs, total)}

**Annual Cost: ${total * 12:.2f}**

### Free AWS Services Included

The following services are included at **no additional cost**:

| Service | Usage | Value |
|---------|-------|-------|
| SSM Session Manager | Unlimited sessions | Replaces bastion host (~$10/month) |
| SSM Patch Manager | Automated patching | Replaces manual patching time |
| SSM Inventory | Resource tracking | Replaces third-party tools |
| SSM Maintenance Windows | Scheduled tasks | Built-in automation |
| S3 Gateway Endpoint | Package downloads | Replaces NAT data charges |

### Cost Optimization

Current configuration saves **~$48/month** by:
- ❌ No NAT Gateway (-$48.18/month)
- ✅ VPC Endpoints for AWS services
- ✅ S3 Gateway Endpoint (free) for package repos
- ✅ Private subnets only (no public IPs)

See [COST-ESTIMATE.md](COST-ESTIMATE.md) for detailed optimization options.
"""
    
    # Replace sections more carefully
    # Architecture section - find and replace everything until next ## heading
    arch_start = content.find('## Architecture')
    if arch_start != -1:
        # Find the next ## heading after Architecture
        next_section = content.find('\n## ', arch_start + 1)
        if next_section != -1:
            content = content[:arch_start] + architecture_section + '\n' + content[next_section+1:]
        else:
            # No next section, replace to end
            content = content[:arch_start] + architecture_section
    
    # Cost section - find and replace everything until next ## heading
    cost_start = content.find('## Cost Breakdown')
    if cost_start != -1:
        # Find the next ## heading after Cost Breakdown
        next_section = content.find('\n## ', cost_start + 1)
        if next_section != -1:
            content = content[:cost_start] + cost_section + '\n' + content[next_section+1:]
        else:
            # No next section, append
            content = content[:cost_start] + cost_section
    else:
        # Add cost section before "Customization" if it doesn't exist
        custom_start = content.find('## Customization')
        if custom_start != -1:
            content = content[:custom_start] + cost_section + '\n\n' + content[custom_start:]
    
    # Write updated README
    with open(readme_path, 'w') as f:
        f.write(content)
    
    return True


def main():
    print("📖 Updating README.md with current infrastructure...")
    
    # Load metadata
    metadata = load_metadata()
    if not metadata:
        return
    
    # Calculate costs
    print("💰 Calculating costs...")
    costs, total = calculate_costs(metadata)
    
    # Update README
    print("✍️  Updating README.md...")
    if update_readme(metadata, costs, total):
        print(f"\n✅ README.md updated successfully!")
        print(f"\nCurrent monthly cost: ${total:.2f}")
        print(f"Annual cost: ${total * 12:.2f}")
        
        # Show breakdown
        print("\nCost breakdown:")
        for category, items in costs.items():
            if items:
                category_total = sum(item['cost'] for item in items)
                print(f"  {category.title()}: ${category_total:.2f}")
    else:
        print("❌ Failed to update README.md")


if __name__ == "__main__":
    main()
