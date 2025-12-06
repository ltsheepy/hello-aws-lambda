# S3 bucket for SSM logs
resource "aws_s3_bucket" "ssm_logs" {
  bucket = "${var.project_name}-ssm-logs-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name        = "${var.project_name}-ssm-logs"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket_versioning" "ssm_logs" {
  bucket = aws_s3_bucket.ssm_logs.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "ssm_logs" {
  bucket = aws_s3_bucket.ssm_logs.id

  rule {
    id     = "delete-old-logs"
    status = "Enabled"

    filter {}

    expiration {
      days = var.log_retention_days
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }
  }
}

resource "aws_s3_bucket_public_access_block" "ssm_logs" {
  bucket = aws_s3_bucket.ssm_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ssm_logs" {
  bucket = aws_s3_bucket.ssm_logs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# S3 bucket policy to allow SSM to write
resource "aws_s3_bucket_policy" "ssm_logs" {
  bucket = aws_s3_bucket.ssm_logs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "SSMBucketPermissionsCheck"
        Effect = "Allow"
        Principal = {
          Service = "ssm.amazonaws.com"
        }
        Action   = "s3:GetBucketAcl"
        Resource = aws_s3_bucket.ssm_logs.arn
      },
      {
        Sid    = "SSMBucketDelivery"
        Effect = "Allow"
        Principal = {
          Service = "ssm.amazonaws.com"
        }
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.ssm_logs.arn}/*"
        Condition = {
          StringEquals = {
            "s3:x-amz-acl" = "bucket-owner-full-control"
          }
        }
      }
    ]
  })
}

# Get current AWS account ID
data "aws_caller_identity" "current" {}
