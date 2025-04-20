variable "region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "mb-api"
}

variable "image_tag" {
  type    = string
  default = "latest"
}

variable "memcached_cpu" {
  description = "vCPU (units) for memcached container"
  type        = number
  default     = 256
}

variable "memcached_memory" {
  description = "Memory (MiB) for memcached container"
  type        = number
  default     = 512
}
