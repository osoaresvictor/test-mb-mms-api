resource "aws_ecs_task_definition" "mb_api_task" {
  family                   = "${var.project_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "${var.project_name}-container"
      image     = "${aws_ecr_repository.mb_api.repository_url}:${var.image_tag}"
      essential = true

      portMappings = [
        { containerPort = 8000, protocol = "tcp" }
      ]

      environment = [
        { name = "ENV", value = "prod" },
        { name = "DB_URL", value = "sqlite:///./test.db" },
        { name = "CACHE_HOST", value = "memcached.svc.local" },
        { name = "CACHE_PORT", value = "11211" },
        { name = "LOG_LEVEL", value = "INFO" },
        { name = "ALLOWED_PAIRS", value = "BRLBTC,BRLETH" },
        { name = "MB_API_BASE_URL", value = "https://mobile.mercadobitcoin.com.br" }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs_logs.name
          "awslogs-region"        = var.region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}
