# Create multiple maintenance windows based on configuration
resource "aws_ssm_maintenance_window" "windows" {
  for_each = var.maintenance_windows

  name              = "${var.project_name}-${each.key}-patching-window"
  description       = "Maintenance window for ${each.key} environment patching"
  schedule          = each.value.schedule
  duration          = each.value.duration
  cutoff            = each.value.cutoff
  schedule_timezone = each.value.timezone

  tags = {
    Name        = "${var.project_name}-${each.key}-patching-window"
    Environment = each.key
    ManagedBy   = "Terraform"
  }
}

# Targets for each maintenance window
resource "aws_ssm_maintenance_window_target" "targets" {
  for_each = var.maintenance_windows

  window_id     = aws_ssm_maintenance_window.windows[each.key].id
  name          = "${var.project_name}-${each.key}-targets"
  description   = "Instances in ${each.key} patch group"
  resource_type = "INSTANCE"

  targets {
    key    = "tag:PatchGroup"
    values = [each.value.patch_group]
  }
}

# Patch tasks for each maintenance window
resource "aws_ssm_maintenance_window_task" "patch_tasks" {
  for_each = var.maintenance_windows

  window_id        = aws_ssm_maintenance_window.windows[each.key].id
  name             = "${var.project_name}-${each.key}-patch-task"
  description      = "Apply OS patches for ${each.key} environment"
  task_type        = "RUN_COMMAND"
  task_arn         = "AWS-RunPatchBaseline"
  priority         = 1
  service_role_arn = aws_iam_role.ssm_maintenance.arn
  max_concurrency  = each.value.max_concurrency
  max_errors       = each.value.max_errors

  targets {
    key    = "WindowTargetIds"
    values = [aws_ssm_maintenance_window_target.targets[each.key].id]
  }

  task_invocation_parameters {
    run_command_parameters {
      parameter {
        name   = "Operation"
        values = ["Install"]
      }

      parameter {
        name   = "RebootOption"
        values = [each.value.reboot_option]
      }

      output_s3_bucket     = aws_s3_bucket.ssm_logs.id
      output_s3_key_prefix = "maintenance-windows/${each.key}/"

      cloudwatch_config {
        cloudwatch_log_group_name = aws_cloudwatch_log_group.ssm_maintenance[each.key].name
        cloudwatch_output_enabled = true
      }
    }
  }
}

# Patch Baselines for each environment
resource "aws_ssm_patch_baseline" "baselines" {
  for_each = var.maintenance_windows

  name             = "${var.project_name}-${each.key}-al2023-baseline"
  description      = "Patch baseline for ${each.key} Amazon Linux 2023 instances"
  operating_system = "AMAZON_LINUX_2023"

  approval_rule {
    approve_after_days = each.value.approval_days
    compliance_level   = each.key == "critical" ? "CRITICAL" : "HIGH"

    patch_filter {
      key    = "CLASSIFICATION"
      values = ["Security", "Bugfix", "Enhancement"]
    }

    patch_filter {
      key    = "SEVERITY"
      values = each.key == "critical" ? ["Critical"] : ["Critical", "Important", "Medium"]
    }
  }

  tags = {
    Name        = "${var.project_name}-${each.key}-baseline"
    Environment = each.key
    ManagedBy   = "Terraform"
  }
}

# Register patch baselines with patch groups
resource "aws_ssm_patch_group" "groups" {
  for_each = var.maintenance_windows

  baseline_id = aws_ssm_patch_baseline.baselines[each.key].id
  patch_group = each.value.patch_group
}

# CloudWatch Log Groups for each maintenance window
resource "aws_cloudwatch_log_group" "ssm_maintenance" {
  for_each = var.maintenance_windows

  name              = "/aws/ssm/maintenance-windows/${var.project_name}/${each.key}"
  retention_in_days = var.log_retention_days

  tags = {
    Name        = "${var.project_name}-${each.key}-ssm-logs"
    Environment = each.key
    ManagedBy   = "Terraform"
  }
}
