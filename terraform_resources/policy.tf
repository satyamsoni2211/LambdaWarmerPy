data "aws_iam_policy_document" "event_trust_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "event_trigger_policy" {
    statement {
      actions = ["lambda:invokeFunction"]
      effect = "Allow"
      resources = [ var.arn ]
    }
}

resource "aws_iam_role" "warmer-lambda-trigger-role" {
  name               = "warmer-lambda-trigger-role"
  assume_role_policy = data.aws_iam_policy_document.event_trust_policy.json
}
resource "aws_iam_policy" "lambda-trigger-permission-policy" {
    name = "lambda-trigger-permission-policy"
    policy = data.aws_iam_policy_document.event_trigger_policy.json
}
resource "aws_iam_role_policy_attachment" "attach-warmer-policy" {
  role = aws_iam_role.warmer-lambda-trigger-role.name
  policy_arn = aws_iam_policy.lambda-trigger-permission-policy.arn
}