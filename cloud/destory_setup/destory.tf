# Provider Configuration
provider "aws" {
  region = var.aws_region
}

# Modules to Destroy
module "vpc" {
  source                 = "./modules/vpc"
  name                   = "ecommerce-vpc"
  cidr_block             = "10.0.0.0/16"
  public_subnet_cidrs    = ["10.0.1.0/24", "10.0.2.0/24"]
  azs                    = ["ap-southeast-2a", "ap-southeast-2b"]
  environment            = "dev"
}

module "ec2_instance" {
  source        = "./modules/ec2"
  name          = "ecommerce-ec2"
  ami_id        = var.ami_id
  instance_type = "t3.micro"
  subnet_id     = module.vpc.public_subnet_ids[0]
  vpc_id        = module.vpc.vpc_id
}

# Outputs
output "destroy_message" {
  value = <<EOT
  All VPC and EC2 resources will be destroyed. Ensure no dependent resources exist before proceeding.
  VPC: ${module.vpc.name}
  EC2 Instance: ${module.ec2_instance.name}
  EOT
}
