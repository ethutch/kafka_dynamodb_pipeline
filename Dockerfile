FROM public.ecr.aws/lambda/python:3.11

# Copy project definition
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy application source code under package namespace
COPY kafka_dynamodb_pipeline/ ${LAMBDA_TASK_ROOT}/kafka_dynamodb_pipeline/

CMD [ "kafka_dynamodb_pipeline.consumer.app.handler" ]
