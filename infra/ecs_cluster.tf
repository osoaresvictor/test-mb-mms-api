resource "aws_ecs_cluster" "mb_api_cluster" {
  name = "${var.project_name}-cluster"
}
