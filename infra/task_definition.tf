resource "aws_ecs_task_definition" "mb_api_task" {
  family                   = "mb-api-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "mb-api-container"
      image     = "123456789012.dkr.ecr.us-east-1.amazonaws.com/mb-api:latest"
      essential = true

      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]

      environment = [
        { name = "ENV", value = "prod" },
        { name = "DB_URL", value = "sqlite:///./test.db" },
        { name = "CACHE_HOST", value = "localhost" },
        { name = "CACHE_PORT", value = "11211" },
        { name = "LOG_LEVEL", value = "INFO" },
        { name = "ALLOWED_PAIRS", value = "BRLBTC,BRLETH" },
        { name = "MB_API_BASE_URL", value = "https://mobile.mercadobitcoin.com.br" }
      ]
    }
  ])
}
