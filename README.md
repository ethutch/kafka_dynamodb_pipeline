# Kafka → DynamoDB Event Pipeline

An enterprise-grade, event-driven Python pipeline that consumes Protobuf-serialized messages from Apache Kafka, deserializes and validates events using Pydantic models, and persists records to Amazon DynamoDB via AWS Lambda and LocalStack.

Note that due to a limitation in Local-Stack does not support AWS Event Source Mapping (ESM).
Therefore to make the local system work the kafka_mongo_pipeline project is used to emulate this
function.

In real AWS ESM would consume the kafka topic messages and present them to the lambda.  Since that
cannot be emulated with the selected local tools the kafka_mongo_pipeline has been enhanced to 
perform the function of ESM.  Specifically after it consumes a message and performs all its normal
processing it will format an *exact* representation of the ESM payload and directly invoke this 
lambda.  Because of the control flow the only difference is that the ESM payload from AWS can contain
more than one kafka message, but in this design only one message (record in ESM parlance) will ever
be passed.  However the full processing loop for N records is implemented in all respects.

---

## Architecture Overview
<pre style="background: transparent;"><code>
+-----------------------------------------------------------------------------------+
| Host Machine / Docker Network                                                     |
|                                                                                   |
|  +-----------------+      +--------+              +-----------------------+       |
|  | Kafka Container |  <== | Python |  ==========> | LocalStack Container  |       |
|  | (Port 9092)     |      | Poller |       ESM    |                       |       |
|  +-----------------+      +--------+    emulation |  - Lambda Exec Engine |       |
|            |                                      +-----------------------+       |
|            |                                        |                             |         
|            |                                        | Writes Records              |
|            |                                        v                             |
|            |                    +-----------------------+                         |
|            |                    | DynamoDB Container    | (External Container     |
|            +------------------> | (Port 8000 / 4566)    |  with Persistent        |
|                                 +-----------------------+  Volume Storage)        |
+-----------------------------------------------------------------------------------+
</code></pre>
---
# Repository Structure
<pre style="background: transparent;"><code>
kafka-dynamodb-pipeline/
├── src/ 
│   └── kafka_dynamodb_pipeline/    # Main application package namespace
│       ├── main.py                 # Application Entry Point & AWS Lambda Handler
│       ├── event_deserializer.py   # Apicurio schema validation and protobuf deserialization
│       ├── exceoptions.py          # Custom exceptions
│       ├── config/                 # Pydantic Settings & Environment Management
│       │   └── settings.py
│       ├── models/                 # Pydantic Domain Models & Mappers
│       │   ├── customer_event.py
│       │   ├── esm_kafka_event.py  # This is what ESM would have produced if it existed
│       │   ├── order_event.py
│       │   └── processing_result.py
│       ├── proto/                  # Generated Protobuf Python Stubs & Definitions
│       │   ├── customer_event_pb2.py
│       │   ├── customer_event_pb2.pyi
│       │   ├── customer_event.proto
│       │   ├── order_event_pb2.py
│       │   ├── order_event_pb2.pyi
│       │   └── order_event.proto
│       └── utils/                  # Structlog Configuration & Common Helpers
│           ├── logger.py
│           └── logging.py
├── tests/                          # Unit and Integration Test Suites
│   ├── conftest.py
│   ├── test_consumer.py
│   └── test_models.py
├── tofu/                           # OpenTofu / Terraform Infrastructure Specs
│   ├── dynamodd.tf
│   ├── iam.tf
│   ├── lambda.tf
│   ├── lambda.tf_miltilayer-is-unsupported    # multilayer doesn't work in local-stack
│   ├── local.tfvars
│   ├── providers.tf
│   ├── variables.tf
│   └── versions.tf
├── Dockerfile                      # Production AWS Lambda Container Image
├── esmMessage.json                 # Sample event source mapping message
├── rawMessage.json                 # Sample raw Kafka message
├── README.md                       # This file
└── pyproject.toml                  # Build backend configuration & dependency specifications
</code></pre>
---

## Quick Start

### 1. Prerequisites
- Python: 3.13+
- Docker & Docker Compose
- OpenTofu / Terraform (for infrastructure provisioning)
- Protocol Buffers Compiler (`protoc`)
- `kcat` / `kafkacat` (optional, for raw topic inspection)

### 2. Local Environment Setup

# Clone the repository and navigate to root
```cd kafka-dynamodb-pipeline```

# Create and activate virtual environment
```
python -m venv .venv
source .venv/bin/activate
```

# Install application and dev dependencies
```pip install -e ".[dev]"```

---

## Dependency Management & Build Tooling

To inspect the current dependency tree:

```pipdeptree```

To update dependencies after modifying pyproject.toml:

```pip install -e ".[dev]"```

To build and deploy:

``` tofu apply -var-file=local.tfvars```
---

## Code Generation (Protobuf)

Compile `.proto` schema files into Python classes (`_pb2.py`) and type hint interfaces (`_pb2.pyi`):

```
protoc -I=kafka_dynamodb_pipeline/proto --python_out=kafka_dynamodb_pipeline/proto --pyi_out=kafka_dynamodb_pipeline/proto customer_event.proto
```
---
## Useful CLI Commands
Execute with sample payload:
```
aws --endpoint-url=http://localhost:4566 lambda invoke --function-name kafka-dynamodb-pipeline --payload fileb://esmMessage.json /tmp/lambda-response.json
```

Since there is no web interface logs are a little painful.
1. Find the log group.  This is really pretty obvious but shown for completeness
```
aws --endpoint-url=http://localhost:4566 logs describe-log-groups --log-group-name-prefix /aws/lambda/kafka-dynamodb-pipeline
```
2. Get all the log streams.  This part you need!
```
aws --endpoint-url=http://localhost:4566 logs describe-log-groups --log-group-name-prefix /aws/lambda/kafka-dynamodb-pipeline
```
3. Display the log data.  You probably want the first one on the list
```
aws --endpoint-url=http://localhost:4566 logs get-log-events \
  --log-group-name /aws/lambda/kafka-dynamodb-pipeline \
  --log-stream-name '<NAME from the list in step 2>' \
  --start-from-head
```
4. You can also display records saved to DynamoDB:
```
aws --endpoint-url=http://localhost:8000 dynamodb get-item --table-name customers --key '{"customerId": {"S": "<known partition key here>"}}'
```
---

## Infrastructure & Local Deployment

### 1. Start Local Infrastructure

This project asssumes you already have Docker running with containers for: Kafka, standalone DynamoDB Local, and LocalStack


### 2. Provision AWS Resources via OpenTofu

Deploy the DynamoDB table, IAM execution roles, Lambda function, and Kafka Event Source Mapping into LocalStack:
```
$ cd tofu
$ tofu init
$ tofu apply -auto-approve \
    -var-file=local.tfvars
$ cd ..
```
---


## Testing & Static Analysis

This project uses `pytest`, `pytest-cov`, `ruff`, and `mypy` to enforce code quality, static typing, and test coverage across unit and integration boundaries.

### Prerequisites

Ensure development dependencies are installed in your active virtual environment:

`pip install -e ".[dev]"`

### Running Test Suites

Execute the full test suite across all modules:

`pytest`

Execute unit tests in isolation (uses `moto` via `conftest.py` to mock AWS DynamoDB):

`pytest tests/test_consumer.py -v`

### Test File Breakdown

- **`tests/conftest.py`**: Shared `pytest` configuration and fixtures. Automatically loaded by `pytest` to set up mock AWS DynamoDB environments via `moto`, mock Kafka event payloads, and environment settings.
- **`tests/test_models.py`**: Unit tests for Pydantic schema constraints, string trimming/casing sanitization, and settings-driven `field_validator` logic.

### Static Analysis & Type Checking

Run linting checks:

`ruff check .`

Run code formatting checks:

`ruff format . --check`

Run strict static type checking across the codebase:

`mypy .`

### Code Coverage

Execute the test suite and generate terminal coverage metrics:

`coverage run -m pytest`
`coverage report -m`

Or generate coverage directly using `pytest-cov`:

`pytest --cov=. --cov-report=term-missing`

Generate an HTML report for visual inspection in a browser (saved to `htmlcov/index.html`):

`pytest --cov=. --cov-report=html`

## Testing the Install

Afer running tofu apply you can test the lambda by invoking from the cli with a dummy payload:

```
aws --endpoint-url=http://localhost:4566 lambda invoke --function-name kafka-dynamodb-pipeline --cli-binary-format raw-in-base64-out  --payload '{"test": "data"}' response.json
```
The expected response is:
```
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}
```