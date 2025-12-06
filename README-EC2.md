# CIS Hardened Amazon Linux Instance

A production-ready, CIS-hardened EC2 instance with SSM access (no SSH).

## Features

- **CIS Hardened AMI**: Official CIS Amazon Linux 2023 benchmark image
- **SSM Access**: Connect via AWS Systems Manager (no SSH keys needed)
- **Security**:
  - No inbound ports open
  - IMDSv2 enforced
  - Encrypted root volume
  - Minimal security group (HTTPS/HTTP outbound only)

## Deploy

```bash
terraform init
terraform plan
terraform apply
```

## Connect to Instance

After deployment, Terraform will output the connection command:

```bash
aws ssm start-session --target i-xxxxxxxxx --region ap-southeast-2
```

Or install the Session Manager plugin first:
```bash
# macOS
brew install --cask session-manager-plugin
```

## What's Included

- **No SSH**: Uses SSM Session Manager instead
- **Encrypted storage**: Root volume encrypted at rest
- **IMDSv2**: Instance metadata v2 enforced
- **Minimal permissions**: Only SSM access granted
- **CIS compliance**: Pre-hardened OS image

## Clean Up

```bash
terraform destroy
```

## Cost

t3.micro in Sydney: ~$0.0136/hour (~$10/month if running 24/7)
