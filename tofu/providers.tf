provider "aws" {
  region                      = var.aws_region
  access_key                  = "mockkey"
  secret_key                  = "mockkey"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    apigateway     = var.localstack_endpoint
    dynamodb       = var.dynamodb_endpoint
    events         = var.localstack_endpoint
    iam            = var.localstack_endpoint
    lambda         = var.localstack_endpoint
    s3             = var.localstack_endpoint
    secretsmanager = var.localstack_endpoint
    sqs            = var.localstack_endpoint
    sts            = var.localstack_endpoint
  }
}