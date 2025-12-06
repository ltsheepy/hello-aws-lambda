#!/usr/bin/env python3
"""
Generate AWS architecture diagram for CIS Hardened Infrastructure
Requires: pip install diagrams
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import VPC, PrivateSubnet, Endpoint
from diagrams.aws.security import IAMRole
from diagrams.aws.management import SystemsManager, CloudwatchAlarm, Cloudwatch
from diagrams.aws.storage import S3

# Diagram attributes
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
    
    # User/Admin
    admin = SystemsManager("AWS Console\n/ CLI")
    
    with Cluster("VPC (10.0.0.0/16)\nSydney (ap-southeast-2)"):
        
        with Cluster("Private Subnets Only\n10.0.101.0/24, 10.0.102.0/24\n(No Internet Gateway)"):
            private_subnet = PrivateSubnet("Private Subnet")
            
            # EC2 Instance
            with Cluster("EC2 Instance"):
                instance = EC2("Amazon Linux 2023\nt3.micro\n30GB Encrypted")
                instance_role = IAMRole("EC2 SSM Role")
            
            # VPC Endpoints
            with Cluster("VPC Endpoints (Interface)"):
                ssm_endpoint = Endpoint("SSM")
                ssmmsg_endpoint = Endpoint("SSM Messages")
                ec2msg_endpoint = Endpoint("EC2 Messages")
            
            # S3 Gateway Endpoint
            s3_endpoint = Endpoint("S3 Gateway\nEndpoint\n(Free)")
    
    # SSM Services
    with Cluster("AWS Systems Manager"):
        ssm = SystemsManager("Session Manager")
        patch_mgr = SystemsManager("Patch Manager")
        inventory = SystemsManager("Inventory")
        
        with Cluster("Maintenance Windows"):
            mw_prod = SystemsManager("Production\nSun 2AM")
            mw_dev = SystemsManager("Development\nSat 3AM")
            mw_crit = SystemsManager("Critical\nTue 1AM")
    
    # Storage & Monitoring
    with Cluster("Logging & Storage"):
        s3_logs = S3("SSM Logs\n(Encrypted)")
        cw_logs = Cloudwatch("CloudWatch\nLogs")
        cw_alarm = CloudwatchAlarm("Billing\nAlerts")
    
    # S3 for packages
    s3_repos = S3("Amazon Linux\nRepositories")
    
    # Connections
    admin >> Edge(label="SSM Session") >> ssm
    ssm >> Edge(label="via VPC Endpoints") >> ssm_endpoint
    ssm_endpoint >> Edge(label="Private") >> instance
    ssmmsg_endpoint >> instance
    ec2msg_endpoint >> instance
    
    instance >> Edge(label="Assume Role") >> instance_role
    
    patch_mgr >> Edge(label="Patch Tasks") >> [mw_prod, mw_dev, mw_crit]
    [mw_prod, mw_dev, mw_crit] >> Edge(label="Target by\nPatchGroup Tag") >> instance
    
    inventory >> Edge(label="Collect every\n30 minutes") >> instance
    
    instance >> Edge(label="Logs") >> s3_logs
    instance >> Edge(label="Logs") >> cw_logs
    
    instance >> Edge(label="Package Updates\n(Private)") >> s3_endpoint
    s3_endpoint >> Edge(label="Gateway\n(Free)") >> s3_repos

print("✅ Architecture diagram generated: architecture.png")
print("\nKey Features:")
print("- Private subnets only (no internet gateway)")
print("- No NAT Gateway (saves $48/month)")
print("- VPC Endpoints for SSM access")
print("- S3 Gateway Endpoint for package updates (free)")
print("- Tag-based maintenance windows")
print("- Encrypted storage and logs")
print("- Fully isolated from internet")
print("\nEstimated Cost: ~$36/month")
