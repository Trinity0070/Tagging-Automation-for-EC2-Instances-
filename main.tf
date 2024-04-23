# Lambda function resource
resource "aws_lambda_function" "tag_ec2_lambda" {
  function_name    = "tag_ec2_lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.8"
  filename         = "lambda_function.zip"
  # source_code_hash = filebase64sha256("${path.module}/lambda_function.zip")
}

resource "aws_cloudwatch_event_rule" "ec2_run_instance_rule" {
  name          = "TriggerLambdaOnEC2RunInstance"
  description   = "Trigger Lambda function when an EC2 instance is launched"
  event_pattern = <<PATTERN
{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "ec2.amazonaws.com"
    ],
    "eventName": [
      "RunInstances "
    ]
  }
}
PATTERN
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.ec2_run_instance_rule.name
  target_id = "TagEC2Lambda"
  arn       = aws_lambda_function.tag_ec2_lambda.arn
}

# Lambda function permission to invoke
resource "aws_lambda_permission" "allow_ec2_trigger" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tag_ec2_lambda.arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ec2_run_instance_rule.arn
}

