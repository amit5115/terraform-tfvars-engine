output "server_ips" {
  value = aws_instance.server[*].public_ip
}
