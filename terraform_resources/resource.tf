resource "aws_cloudwatch_event_rule" "trigger_lambda" {
  name = "warm-lambda-function"
  schedule_expression = "cron(*/5 * ? * 2-6 *)"
  description = <<-PATTERN
  This resource rule is responsible for warming up lambda function
  PATTERN
  is_enabled = true
  tags = {
    "Type" = "warmer"
    "Provisioner" = "Terraform"
  }
  role_arn = aws_iam_role.warmer-lambda-trigger-role.arn
}

locals {
  function_name=split(":",var.arn)[6]
}

resource "aws_cloudwatch_event_target" "lambda_warmer_target" {
  target_id = "LambdaWarmer-${local.function_name}"
  arn = var.arn
  rule = aws_cloudwatch_event_rule.trigger_lambda.name
  input = <<-INPUT
  {
    "warmer": true
  }
  INPUT
}

resource "aws_lambda_permission" "allow_cloudwatch_trigger" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = local.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.trigger_lambda.arn
}
