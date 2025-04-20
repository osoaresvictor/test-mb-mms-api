output "cluster_name" {
  value = aws_ecs_cluster.mb_api_cluster.name
}

output "ecr_repository_url" {
  value = aws_ecr_repository.mb_api.repository_url
}

output "public_subnet_id" {
  value = aws_subnet.main.id
}

output "web_security_group_id" {
  value = aws_security_group.ecs_service.id
}

