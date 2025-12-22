terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}


provider "aws" {
  region = "ap-south-1"
  

}

resource "aws_instance" "server" {
  count         = var.server_count
  ami           = var.ami_id  # example AMI
  instance_type = var.instance_type

  tags = var.tags
}
