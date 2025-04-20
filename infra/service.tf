resource "aws_ecs_service" "mb_api_service" {
  name            = "mb-api-service"
  cluster         = aws_ecs_cluster.mb_api_cluster.id
  task_definition = aws_ecs_task_definition.mb_api_task.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets          = var.subnets
    assign_public_ip = true
    security_groups  = var.security_groups
  }
}
