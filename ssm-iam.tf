# IAM role for SSM Maintenance Windows
resource "aws_iam_role" "ssm_maintenance" {
  name = "${var.project_name}-ssm-maintenance-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ssm.amazonaws.com"
      }
    }]
  })

  tags = {
    Name        = "${var.project_name}-ssm-maintenance-role"
    Environment = var.environment
  }
}

# Policy for maintenance window execution
resource "aws_iam_role_policy" "ssm_maintenance" {
  name = "${var.project_name}-ssm-maintenance-policy"
  role = aws_iam_role.ssm_maintenance.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:SendCommand",
          "ssm:GetCommandInvocation",
          "ssm:ListCommandInvocations",
          "ssm:ListCommands"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances",
          "ec2:DescribeInstanceStatus"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject"
        ]
        Resource = "${aws_s3_bucket.ssm_logs.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "${aws_cloudwatch_log_group.ssm_maintenance.arn}:*"
      }
    ]
  })
}

# Add S3 permissions to EC2 instance role for SSM logs
resource "aws_iam_role_policy" "ec2_ssm_s3" {
  name = "${var.project_name}-ec2-ssm-s3-policy"
  role = aws_iam_role.ec2_ssm.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject"
        ]
        Resource = "${aws_s3_bucket.ssm_logs.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams"
        ]
        Resource = "${aws_cloudwatch_log_group.ssm_maintenance.arn}:*"
      }
    ]
  })
}
