locals {
  dotenv = {
    for line in split("\n", file("${path.module}/../.env")) :
    trimspace(split("=", trimspace(line))[0]) => trimspace(
      join("=", slice(
        split("=", trimspace(line)),
        1,
        length(split("=", trimspace(line)))
      ))
    )
    if length(split("=", trimspace(line))) > 1 &&
    !startswith(trimspace(line), "#")
  }
}

# 1. Build code AND dependencies together in one clean directory
resource "null_resource" "build_lambda_package" {
  triggers = {
    source_hash = sha256(join("", [
      for file in sort(fileset("${path.module}/../src", "**"))
      : filesha256("${path.module}/../src/${file}")
    ]))

    dependencies_hash = filesha256("${path.module}/../pyproject.toml")
  }




  provisioner "local-exec" {
    command = <<-EOT
      # 1. Clean slate
      rm -rf ${path.module}/build_staging
      mkdir -p ${path.module}/build_staging

      # 2. Copy ONLY your source code
      cp -r ${path.module}/../src/* ${path.module}/build_staging/

      # 3. Extract ONLY production dependencies (no dev!)
      python3 -c "
import tomllib
with open('${path.module}/../pyproject.toml', 'rb') as f:
    data = tomllib.load(f)
print('\n'.join(data['project']['dependencies']))
" > ${path.module}/build_staging/requirements.txt

      # 4. Install dependencies directly into the staging directory
      # Native ARM64 build (no --platform flag needed on M3 Mac)
      docker run --rm \
        -v "${path.module}/build_staging:/work" \
        public.ecr.aws/sam/build-python3.13 \
        sh -c "pip install -r /work/requirements.txt --target /work && \
        # Clean up unnecessary bloat to keep zip tiny
        find /work -type d -name '__pycache__' -exec rm -rf {} + && \
        find /work -type d -name '*.dist-info' -exec rm -rf {} + && \
        rm -rf /work/boto3 /work/botocore" # Lambda already has boto3
    EOT
  }
}

# 2. Zip the combined directory with aggressive exclusions
data "archive_file" "lambda_package" {
  type        = "zip"
  source_dir  = "${path.module}/build_staging"
  output_path = "${path.module}/build/kafka_dynamodb_pipeline.zip"

  excludes = [
    "**/__pycache__",
    "**/*.pyc",
    "**/.pytest_cache",
    "**/.mypy_cache",
    "**/.git",
    "**/.venv",
    "**/.DS_Store",
    "**/.coverage",
    "**/htmlcov",
    "**/tests",
    "**/requirements.txt" # Don't need this in the final zip
  ]

  depends_on = [null_resource.build_lambda_package]
}

# 3. Deploy the Lambda (No layers needed!)
resource "aws_lambda_function" "kafka_to_dynamodb" {
  filename         = data.archive_file.lambda_package.output_path
  source_code_hash = data.archive_file.lambda_package.output_base64sha256

  function_name = "kafka-dynamodb-pipeline"
  role          = aws_iam_role.lambda_role.arn
  handler       = "kafka_dynamodb_pipeline.main.handler"
  runtime       = "python3.13"
  architectures = ["arm64"] # 100% Native ARM64

  environment {
    variables = {
      DYNAMODB_TABLE_NAME       = aws_dynamodb_table.customers.name
      DYNAMODB_ENDPOINT_URL     = var.dynamodb_aws_endpoint
      SUPPORTED_CUSTOMER_EVENTS = local.dotenv["SUPPORTED_CUSTOMER_EVENTS"]
      SUPPORTED_ORDER_EVENTS    = local.dotenv["SUPPORTED_ORDER_EVENTS"]
      LOG_LEVEL                 = local.dotenv["LOG_LEVEL"]
    }
  }

  depends_on = [aws_dynamodb_table.customers]
}