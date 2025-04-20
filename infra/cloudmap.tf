resource "aws_service_discovery_private_dns_namespace" "sd_namespace" {
  name        = "svc.local"
  description = "Private DNS namespace for ECS services"
  vpc         = aws_vpc.main.id
}

resource "aws_service_discovery_service" "memcached" {
  name = "memcached"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.sd_namespace.id

    dns_records {
      type = "A"
      ttl  = 10
    }

    routing_policy = "MULTIVALUE"
  }
}
