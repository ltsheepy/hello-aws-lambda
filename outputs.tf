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
