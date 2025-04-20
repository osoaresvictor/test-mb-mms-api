resource "aws_security_group" "ecs_service" {
  name        = "mb-web-sg"
  description = "Allow HTTP (8000)"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow from ALB"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mb-web-sg"
  }
}

resource "aws_security_group" "memcached" {
  name        = "memcached-sg"
  description = "Allow internal access to memcached"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 11211
    to_port         = 11211
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_service.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "memcached-sg"
  }
}
