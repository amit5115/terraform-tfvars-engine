variable "env" {
  description = "Environment name"
  type        = string
}

variable "server_count" {
  description = "Number of servers"
  type        = number
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}
variable "allowed_port" {
  type = list(number)
}
variable "tags" {
  type = map(string)
}
