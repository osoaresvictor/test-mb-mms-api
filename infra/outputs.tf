output "vpc_id" {
  value = aws_vpc.main.id
}

output "cluster_name" {
  value = aws_ecs_cluster.mb_api_cluster.name
}

output "ecr_repository_url" {
  value = aws_ecr_repository.mb_api.repository_url
}

output "web_security_group_id" {
  value = aws_security_group.ecs_service.id
}
