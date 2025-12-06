# SSM Maintenance Windows - Tag-Based Patching

## Overview

This infrastructure uses AWS Systems Manager Maintenance Windows for automated patching, controlled entirely by tags.

## Patch Groups

Three maintenance windows are configured:

### 1. Production
- **Schedule**: Sunday 2 AM (Sydney time)
- **Patch Approval**: 7 days
- **Reboot**: RebootIfNeeded
- **Tag**: `PatchGroup=production`

### 2. Development
- **Schedule**: Saturday 3 AM (Sydney time)
- **Patch Approval**: 3 days (faster updates)
- **Reboot**: RebootIfNeeded
- **Tag**: `PatchGroup=development`

### 3. Critical
- **Schedule**: Tuesday 1 AM (Sydney time)
- **Patch Approval**: 14 days (more testing)
- **Reboot**: NoReboot (manual reboot required)
- **Tag**: `PatchGroup=critical`

## How to Use

### Assign Instance to Patch Group

Simply tag your instance with the desired patch group:

```bash
# Move to production patching
aws ec2 create-tags --resources i-xxxxx --tags Key=PatchGroup,Value=production

# Move to development patching
aws ec2 create-tags --resources i-xxxxx --tags Key=PatchGroup,Value=development

# Move to critical patching
aws ec2 create-tags --resources i-xxxxx --tags Key=PatchGroup,Value=critical
```

Or in Terraform, set the variable:

```hcl
instance_patch_group = "production"  # or "development" or "critical"
```

### View Maintenance Windows

```bash
aws ssm describe-maintenance-windows --region ap-southeast-2
```

### Check Patch Compliance

```bash
aws ssm describe-instance-patch-states --instance-ids i-xxxxx --region ap-southeast-2
```

### View Patching Logs

**CloudWatch Logs:**
- Production: `/aws/ssm/maintenance-windows/cis-hardened/production`
- Development: `/aws/ssm/maintenance-windows/cis-hardened/development`
- Critical: `/aws/ssm/maintenance-windows/cis-hardened/critical`

**S3 Logs:**
- Bucket: `cis-hardened-ssm-logs-{account-id}`
- Prefix: `maintenance-windows/{environment}/`

## Customize Schedules

Edit `variables.tf` to modify maintenance windows:

```hcl
maintenance_windows = {
  production = {
    schedule        = "cron(0 2 ? * SUN *)"  # Change schedule
    duration        = 3                       # Change duration
    approval_days   = 7                       # Change approval wait
    reboot_option   = "RebootIfNeeded"       # Change reboot behavior
    # ... other settings
  }
}
```

## Manual Patching

To patch immediately outside the maintenance window:

```bash
aws ssm send-command \
  --document-name "AWS-RunPatchBaseline" \
  --targets "Key=tag:PatchGroup,Values=production" \
  --parameters "Operation=Install,RebootOption=NoReboot" \
  --region ap-southeast-2
```

## Cost

- Maintenance Windows: Free
- Patch Manager: Free
- S3 Storage: ~$0.023/GB/month
- CloudWatch Logs: ~$0.50/GB ingested

Estimated: < $5/month for typical usage
