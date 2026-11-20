# DynamoDB table. Hash key = customer_id. GSI allows querying by
# company_name without a full table scan.
#
# LocalStack has a bug and cannot handle GSI!
# So create the table manually and then import it to terraform with:
# tofu import aws_dynamodb_table.customers customers
#
resource "aws_dynamodb_table" "customers" {
  name         = "customers"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "customer_id"

  attribute {
    name = "customer_id"
    type = "S"
  }

  attribute {
    name = "company_name"
    type = "S"
  }

  global_secondary_index {
    name            = "company_name_index"
    hash_key        = "company_name"
    projection_type = "ALL"
  }

  #  lifecycle {
  #   prevent_destroy = true
  # }

}