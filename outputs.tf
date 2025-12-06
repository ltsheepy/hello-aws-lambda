output "instance_id" {
  description = "Instance ID for SSM connection"
  value       = aws_instance.hardened.id
}

output "instance_private_ip" {
  description = "Private IP address of the instance"
  value       = aws_instance.hardened.private_ip
}

output "ssm_connect_command" {
  description = "Command to connect via SSM"
  value       = "aws ssm start-session --target ${aws_instance.hardened.id} --region ${var.aws_region}"
}

output "ami_used" {
  description = "CIS AMI used"
  value       = data.aws_ami.amazon_linux_cis.name
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "private_subnets" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnets
}

output "maintenance_windows" {
  description = "Map of maintenance window IDs"
  value = {
    for k, v in aws_ssm_maintenance_window.windows : k => {
      id       = v.id
      schedule = v.schedule
      timezone = v.schedule_timezone
    }
  }
}

output "patch_baselines" {
  description = "Map of patch baseline IDs"
  value = {
    for k, v in aws_ssm_patch_baseline.baselines : k => {
      id            = v.id
      approval_days = v.approval_rule[0].approve_after_days
    }
  }
}

output "instance_patch_group" {
  description = "Patch group assigned to the instance"
  value       = var.instance_patch_group
}

output "manual_scan_command" {
  description = "Command to manually trigger a patch scan"
  value       = "aws ssm send-command --document-name AWS-RunPatchBaseline --targets Key=tag:PatchGroup,Values=${var.instance_patch_group} --parameters Operation=Scan --region ${var.aws_region}"
}

output "view_compliance_command" {
  description = "Command to view patch compliance"
  value       = "aws ssm describe-instance-patch-states --instance-ids ${aws_instance.hardened.id} --region ${var.aws_region}"
}

output "ssm_logs_bucket" {
  description = "S3 bucket for SSM logs"
  value       = aws_s3_bucket.ssm_logs.id
}
