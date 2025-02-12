# Output the VPC ID
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main_vpc.id
}

# Output the Public Subnet IDs
output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public_subnets[*].id
}

# Output the Private Subnet IDs
output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private_subnets[*].id
}

# Output the Internet Gateway ID
output "internet_gateway_id" {
  description = "ID of the internet gateway"
  value       = aws_internet_gateway.igw.id
}

output "public_security_group_id" {
  description = "Security group ID for public resources"
  value       = aws_security_group.ec2_public_sg.id
}

output "private_security_group_id" {
  description = "Security group ID for private resources"
  value       = aws_security_group.private_rds_sg.id
}
