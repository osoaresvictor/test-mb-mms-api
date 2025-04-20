output "cluster_name" {
  value = aws_ecs_cluster.mb_api_cluster.name
}

output "ecr_repository_url" {
  value = aws_ecr_repository.mb_api.repository_url
}
