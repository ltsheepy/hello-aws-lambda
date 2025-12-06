variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "ap-southeast-2"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnets" {
  description = "Private subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "root_volume_size" {
  description = "Size of root volume in GB"
  type        = number
  default     = 30
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "Production"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "cis-hardened"
}

# SSM Maintenance Window configurations
variable "maintenance_windows" {
  description = "Map of maintenance windows with their configurations"
  type = map(object({
    schedule          = string
    duration          = number
    cutoff            = number
    timezone          = string
    patch_group       = string
    approval_days     = number
    reboot_option     = string
    max_concurrency   = string
    max_errors        = string
  }))
  
  default = {
    production = {
      schedule        = "cron(0 2 ? * SUN *)"  # Sunday 2 AM
      duration        = 3
      cutoff          = 1
      timezone        = "Australia/Sydney"
      patch_group     = "production"
      approval_days   = 7
      reboot_option   = "RebootIfNeeded"
      max_concurrency = "1"
      max_errors      = "1"
    }
    
    development = {
      schedule        = "cron(0 3 ? * SAT *)"  # Saturday 3 AM
      duration        = 2
      cutoff          = 1
      timezone        = "Australia/Sydney"
      patch_group     = "development"
      approval_days   = 3
      reboot_option   = "RebootIfNeeded"
      max_concurrency = "2"
      max_errors      = "1"
    }
    
    critical = {
      schedule        = "cron(0 1 ? * TUE *)"  # Tuesday 1 AM
      duration        = 4
      cutoff          = 1
      timezone        = "Australia/Sydney"
      patch_group     = "critical"
      approval_days   = 14
      reboot_option   = "NoReboot"
      max_concurrency = "1"
      max_errors      = "0"
    }
  }
}

variable "instance_patch_group" {
  description = "Which patch group this instance belongs to"
  type        = string
  default     = "production"
}

variable "enable_s3_gateway_endpoint" {
  description = "Enable S3 gateway endpoint for yum updates"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "Days to retain logs"
  type        = number
  default     = 30
}
