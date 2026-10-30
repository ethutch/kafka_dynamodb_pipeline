# Execution role the Lambda assumes at runtime. Grants ZERO permissions by
# itself — only declares that the Lambda service may assume this identity.
# Actual permissions come from the two role_policy resources below.
resource "aws_iam_role" "lambda_role" {
  name = "kafka_customer_consumer_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# CloudWatch Logs permissions. LocalStack Community does not enforce IAM,
# so this has no local effect — it exists for correctness against real AWS.
resource "aws_iam_role_policy" "lambda_logging" {
  name = "lambda-logging"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      Resource = "arn:aws:logs:*:*:*"
    }]
  })
}

# CRUD on the customers table and its GSI. Scoped to this table only.
resource "aws_iam_role_policy" "lambda_dynamodb" {
  name = "lambda-dynamodb-access"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Query"
      ]
      Resource = [
        aws_dynamodb_table.customers.arn,
        "${aws_dynamodb_table.customers.arn}/index/*"
      ]
    }]
  })
}