variable "env" {
  description = "Environment name"
  type        = string
}

variable "server_count" {
  description = "Number of servers"
  type        = number
}
variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
  
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}
# variable "allowed_port" {
#   type = list(number)
# }
variable "tags" {
  type = map(string)
}
