variable "subnets" {
  type        = list(string)
  description = "List of subnet IDs for ECS service"
}

variable "security_groups" {
  type        = list(string)
  description = "List of security group IDs for ECS service"
}
