#!/usr/bin/env python3
"""
Dynamic AWS architecture diagram generator
Reads from Terraform state to generate accurate diagrams
"""

import json
import subprocess
import sys
from pathlib import Path

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import PrivateSubnet, Endpoint
from diagrams.aws.security import IAMRole
from diagrams.aws.management import SystemsManager, Cloudwatch
from diagrams.aws.storage import S3


def get_terraform_state():
    """Get Terraform state as JSON"""
    try:
        result = subprocess.run(
            ["terraform", "show", "-json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error reading Terraform state: {e}")
        print("Make sure you've run 'terraform apply' first")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing Terraform state: {e}")
        sys.exit(1)


def extract_resources(state):
    """Extract relevant resources from Terraform state"""
    resources = {
        'vpc': None,
        'subnets': [],
        'instances': [],
        'vpc_endpoints': [],
        'maintenance_windows': [],
        's3_buckets': [],
        'has_nat_gateway': False,
        'has_igw': False,
    }
    
    if 'values' not in state or 'root_module' not in state['values']:
        return resources
    
    root = state['values']['root_module']
    
    # Check for child modules (VPC module)
    if 'child_modules' in root:
        for module in root['child_modules']:
            if 'resources' in module:
                for resource in module['resources']:
                    if resource['type'] == 'aws_vpc':
                        resources['vpc'] = resource['values']
                    elif resource['type'] == 'aws_subnet':
                        resources['subnets'].append(resource['values'])
                    elif resource['type'] == 'aws_nat_gateway':
                        resources['has_nat_gateway'] = True
                    elif resource['type'] == 'aws_internet_gateway':
                        resources['has_igw'] = True
    
    # Check root module resources
    if 'resources' in root:
        for resource in root['resources']:
            if resource['type'] == 'aws_instance':
                resources['instances'].append(resource['values'])
            elif resource['type'] == 'aws_vpc_endpoint':
                resources['vpc_endpoints'].append(resource['values'])
            elif resource['type'] == 'aws_ssm_maintenance_window':
                resources['maintenance_windows'].append(resource['values'])
            elif resource['type'] == 'aws_s3_bucket':
                resources['s3_buckets'].append(resource['values'])
    
    return resources


def generate_diagram(resources):
    """Generate diagram from extracted resources"""
    
    vpc_cidr = resources['vpc']['cidr_block'] if resources['vpc'] else "10.0.0.0/16"
    region = "ap-southeast-2"  # Could extract from provider config
    
    graph_attr = {
        "fontsize": "16",
        "bgcolor": "white",
        "pad": "0.5",
    }
    
    with Diagram(
        "CIS Hardened EC2 Infrastructure",
        filename="architecture",
        outformat="png",
        show=False,
        direction="TB",
        graph_attr=graph_attr
    ):
        
        admin = SystemsManager("AWS Console\n/ CLI")
        
        # VPC Cluster
        vpc_label = f"VPC ({vpc_cidr})\n{region}"
        if resources['has_igw']:
            vpc_label += "\n(with Internet Gateway)"
        if resources['has_nat_gateway']:
            vpc_label += "\n(with NAT Gateway)"
        
        with Cluster(vpc_label):
            
            # Subnets
            private_subnets = [s for s in resources['subnets'] if 'private' in s.get('tags', {}).get('Name', '').lower()]
            
            subnet_label = f"Private Subnets ({len(private_subnets)} AZs)"
            if not resources['has_igw']:
                subnet_label += "\n(No Internet Gateway)"
            
            with Cluster(subnet_label):
                private_subnet = PrivateSubnet("Private Subnet")
                
                # EC2 Instances
                instances_cluster = []
                for idx, instance in enumerate(resources['instances']):
                    instance_name = instance.get('tags', {}).get('Name', f'Instance {idx+1}')
                    instance_type = instance.get('instance_type', 't3.micro')
                    patch_group = instance.get('tags', {}).get('PatchGroup', 'N/A')
                    
                    with Cluster(f"{instance_name}\nPatchGroup: {patch_group}"):
                        inst = EC2(f"{instance_type}")
                        role = IAMRole("EC2 SSM Role")
                        instances_cluster.append((inst, role))
                
                # VPC Endpoints
                endpoint_names = []
                for endpoint in resources['vpc_endpoints']:
                    service = endpoint.get('service_name', '').split('.')[-1]
                    endpoint_names.append(service)
                
                if endpoint_names:
                    with Cluster(f"VPC Endpoints ({len(endpoint_names)})"):
                        endpoints = [Endpoint(name.upper()) for name in endpoint_names[:3]]
        
        # SSM Services
        with Cluster("AWS Systems Manager"):
            ssm = SystemsManager("Session Manager")
            patch_mgr = SystemsManager("Patch Manager")
            inventory = SystemsManager("Inventory")
            
            if resources['maintenance_windows']:
                with Cluster(f"Maintenance Windows ({len(resources['maintenance_windows'])})"):
                    mw_list = []
                    for mw in resources['maintenance_windows'][:3]:
                        name = mw.get('name', 'Window').split('-')[-2]
                        schedule = mw.get('schedule', 'N/A')
                        mw_list.append(SystemsManager(f"{name}\n{schedule}"))
        
        # Storage & Monitoring
        with Cluster("Logging & Storage"):
            if resources['s3_buckets']:
                s3_logs = S3(f"SSM Logs\n({len(resources['s3_buckets'])} buckets)")
            cw_logs = Cloudwatch("CloudWatch\nLogs")
        
        s3_repos = S3("Amazon Linux\nRepositories")
        
        # Connections
        admin >> Edge(label="SSM Session") >> ssm
        ssm >> Edge(label="via VPC Endpoints") >> endpoints[0] if endpoint_names else private_subnet
        
        if instances_cluster:
            inst, role = instances_cluster[0]
            if endpoint_names:
                endpoints[0] >> Edge(label="Private") >> inst
            inst >> Edge(label="Assume Role") >> role
            
            if resources['maintenance_windows']:
                patch_mgr >> Edge(label="Patch Tasks") >> mw_list[0] if mw_list else inst
                if mw_list:
                    mw_list[0] >> Edge(label="Target by\nPatchGroup Tag") >> inst
            
            inventory >> Edge(label="Collect every\n30 minutes") >> inst
            
            if resources['s3_buckets']:
                inst >> Edge(label="Logs") >> s3_logs
            inst >> Edge(label="Logs") >> cw_logs
            
            # S3 Gateway endpoint
            if 's3' in endpoint_names:
                s3_idx = endpoint_names.index('s3')
                inst >> Edge(label="Package Updates\n(Private)") >> endpoints[s3_idx]
                endpoints[s3_idx] >> Edge(label="Gateway\n(Free)") >> s3_repos
    
    return True


def generate_metadata(resources):
    """Generate metadata file with resource counts"""
    metadata = {
        "generated_at": subprocess.run(
            ["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
            capture_output=True,
            text=True
        ).stdout.strip(),
        "terraform_workspace": subprocess.run(
            ["terraform", "workspace", "show"],
            capture_output=True,
            text=True
        ).stdout.strip(),
        "resources": {
            "vpc_cidr": resources['vpc']['cidr_block'] if resources['vpc'] else None,
            "subnets": len(resources['subnets']),
            "instances": len(resources['instances']),
            "vpc_endpoints": len(resources['vpc_endpoints']),
            "maintenance_windows": len(resources['maintenance_windows']),
            "s3_buckets": len(resources['s3_buckets']),
            "has_nat_gateway": resources['has_nat_gateway'],
            "has_internet_gateway": resources['has_igw'],
        },
        "instance_details": [
            {
                "name": inst.get('tags', {}).get('Name', 'Unknown'),
                "type": inst.get('instance_type', 'Unknown'),
                "patch_group": inst.get('tags', {}).get('PatchGroup', 'None'),
            }
            for inst in resources['instances']
        ],
        "endpoints": [
            ep.get('service_name', '').split('.')[-1]
            for ep in resources['vpc_endpoints']
        ]
    }
    
    with open('architecture-metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return metadata


def main():
    print("🔍 Reading Terraform state...")
    state = get_terraform_state()
    
    print("📊 Extracting resources...")
    resources = extract_resources(state)
    
    print("🎨 Generating diagram...")
    generate_diagram(resources)
    
    print("📝 Generating metadata...")
    metadata = generate_metadata(resources)
    
    print("\n✅ Architecture diagram generated: architecture.png")
    print("✅ Metadata saved: architecture-metadata.json")
    print("\nResources found:")
    print(f"  - VPC: {resources['vpc']['cidr_block'] if resources['vpc'] else 'None'}")
    print(f"  - Subnets: {len(resources['subnets'])}")
    print(f"  - Instances: {len(resources['instances'])}")
    print(f"  - VPC Endpoints: {len(resources['vpc_endpoints'])}")
    print(f"  - Maintenance Windows: {len(resources['maintenance_windows'])}")
    print(f"  - S3 Buckets: {len(resources['s3_buckets'])}")
    print(f"  - NAT Gateway: {'Yes' if resources['has_nat_gateway'] else 'No'}")
    print(f"  - Internet Gateway: {'Yes' if resources['has_igw'] else 'No'}")
    
    if resources['instances']:
        print("\nInstances:")
        for inst in resources['instances']:
            name = inst.get('tags', {}).get('Name', 'Unknown')
            itype = inst.get('instance_type', 'Unknown')
            patch = inst.get('tags', {}).get('PatchGroup', 'None')
            print(f"  - {name} ({itype}) - PatchGroup: {patch}")


if __name__ == "__main__":
    main()
