# SSM Resource Data Sync for inventory (optional but recommended)
resource "aws_ssm_resource_data_sync" "inventory" {
  name = "${var.project_name}-inventory-sync"

  s3_destination {
    bucket_name = aws_s3_bucket.ssm_logs.bucket
    prefix      = "inventory/"
    region      = var.aws_region
  }
}

# SSM Association for inventory collection
resource "aws_ssm_association" "inventory" {
  name = "AWS-GatherSoftwareInventory"

  targets {
    key    = "tag:PatchGroup"
    values = [for k, v in var.maintenance_windows : v.patch_group]
  }

  schedule_expression = "rate(30 minutes)"

  parameters = {
    applications                = "Enabled"
    awsComponents               = "Enabled"
    customInventory             = "Enabled"
    instanceDetailedInformation = "Enabled"
    networkConfig               = "Enabled"
    services                    = "Enabled"
    windowsUpdates              = "Enabled"
    windowsRoles                = "Enabled"
  }

  compliance_severity = "MEDIUM"

  output_location {
    s3_bucket_name = aws_s3_bucket.ssm_logs.id
    s3_key_prefix  = "inventory-associations/"
  }
}

# SSM Association for patch scanning
resource "aws_ssm_association" "patch_scan" {
  name = "AWS-RunPatchBaseline"

  targets {
    key    = "tag:PatchGroup"
    values = [for k, v in var.maintenance_windows : v.patch_group]
  }

  # Scan daily at midnight
  schedule_expression = "cron(0 0 * * ? *)"

  parameters = {
    Operation = "Scan"
  }

  compliance_severity = "CRITICAL"

  output_location {
    s3_bucket_name = aws_s3_bucket.ssm_logs.id
    s3_key_prefix  = "patch-scans/"
  }
}

# SSM Association for updating SSM Agent
resource "aws_ssm_association" "update_agent" {
  name = "AWS-UpdateSSMAgent"

  targets {
    key    = "tag:PatchGroup"
    values = [for k, v in var.maintenance_windows : v.patch_group]
  }

  schedule_expression = "rate(14 days)"

  compliance_severity = "LOW"

  output_location {
    s3_bucket_name = aws_s3_bucket.ssm_logs.id
    s3_key_prefix  = "ssm-agent-updates/"
  }
}
