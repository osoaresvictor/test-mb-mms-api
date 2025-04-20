resource "aws_ecs_task_definition" "memcached" {
  family                   = "memcached"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.memcached_cpu
  memory                   = var.memcached_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([{
    name      = "memcached"
    image     = "471112751029.dkr.ecr.us-east-1.amazonaws.com/memcached:1.6.15-alpine"
    essential = true

    portMappings = [
      { containerPort = 11211, protocol = "tcp" }
    ]
  }])
}

resource "aws_ecs_service" "memcached" {
  name            = "memcached-service"
  cluster         = aws_ecs_cluster.mb_api_cluster.id
  task_definition = aws_ecs_task_definition.memcached.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.public_a.id, aws_subnet.public_b.id]
    assign_public_ip = false
    security_groups  = [aws_security_group.ecs_service.id]
  }

  service_registries {
    registry_arn = aws_service_discovery_service.memcached.arn
  }

  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 200
}
