# Note that tofu will automatically pick up variables from the file:
# terraform.tfvars
#
# To use this file specifiy:
# tofu apply -var-file=local.tfvars
#
# OR set enironment variables:
#export TF_CLI_ARGS_plan="-var-file=local.tfvars"
#export TF_CLI_ARGS_apply="-var-file=local.tfvars"
#
aws_region          = "us-east-1"
dynamodb_endpoint   = "http://localhost:8000" 
localstack_endpoint = "http://localhost:4566"
dynamodb_aws_endpoint = "http://host.docker.internal:8000"