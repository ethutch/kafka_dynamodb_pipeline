variable "aws_region" {
  type        = string
  description = "AWS region for provider configuration"
  default     = "us-east-1"
}

variable "dynamodb_endpoint" {
  type        = string
  description = "Custom endpoint URL for DynamoDB for tofu to connect"
}
        
variable "dynamodb_aws_endpoint" {
  type        = string
  description = "Custom endpoint URL for DynamoDB for lambda to connect"
}

variable "localstack_endpoint" {
  type        = string
  description = "Endpoint for LocalStack services (IAM, Lambda, etc.)"
  # default     = "http://localhost:4566"
}
