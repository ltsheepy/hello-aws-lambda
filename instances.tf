# EC2 instance with CIS hardened AMI
resource "aws_instance" "hardened" {
  ami                    = data.aws_ami.amazon_linux_cis.id
  instance_type          = var.instance_type
  iam_instance_profile   = aws_iam_instance_profile.ec2.name
  vpc_security_group_ids = [aws_security_group.instance.id]
  subnet_id              = module.vpc.private_subnets[0]

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required" # IMDSv2 only
    http_put_response_hop_limit = 1
  }

  root_block_device {
    volume_type           = "gp3"
    volume_size           = var.root_volume_size
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name        = "${var.project_name}-instance"
    Environment = var.environment
    CIS         = "hardened"
    PatchGroup  = var.instance_patch_group
  }
}
