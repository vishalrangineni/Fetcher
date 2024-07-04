# Data Engineering Take Home: ETL off a SQS Queue

## Setup Instructions

1. Install Docker for Windows.
2. Install AWS CLI Local: `pip install awscli-local`
3. Install PostgreSQL Client.

## Running the Project

1. Start the Docker services:
    ```sh
    docker-compose up -d
    ```

2. Create the SQS queue and load sample data:
    ```sh
    awslocal sqs create-queue --queue-name login-queue --region us-east-1
    awslocal sqs send-message --queue-url http://localhost:4566/000000000000/login-queue --message-body file://sample_message.json --region us-east-1
    ```

3. Create the PostgreSQL table:
    ```sh
    psql -d postgres -U postgres -p 5432 -h localhost -W
    ```

4. Run the ETL process script:
    ```sh
    set AWS_ACCESS_KEY_ID=dummy
    set AWS_SECRET_ACCESS_KEY=dummy
    python etl_process.py
    ```

## Verification

1. Connect to the PostgreSQL database:
    ```sh
    psql -d postgres -U postgres -p 5432 -h localhost -W
    ```

2. Verify the data insertion:
    ```sql
    SELECT * FROM user_logins;
    ```

## Additional Information

- The PII data (`device_id` and `ip`) is masked using SHA-256 hashing to ensure easy identification of duplicates.
- Ensure the Docker services are running before executing the Python script.
