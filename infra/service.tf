resource "aws_ecs_service" "mb_api_service" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.mb_api_cluster.id
  task_definition = aws_ecs_task_definition.mb_api_task.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets = [
      aws_subnet.private_a.id,
      aws_subnet.private_b.id
    ]
    assign_public_ip = false
    security_groups  = [aws_security_group.ecs_service.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.tg.arn
    container_name   = "${var.project_name}-container"
    container_port   = 8000
  }

  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 200
}
