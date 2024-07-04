import json
import hashlib
import boto3
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Configure Boto3 to use dummy credentials
session = boto3.Session(
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

# Connect to localstack SQS
sqs = session.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')

# Connect to Postgres
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

# Function to mask PII
def mask_pii(value):
    return hashlib.sha256(value.encode()).hexdigest()

# Read messages from SQS
response = sqs.receive_message(
    QueueUrl='http://localhost:4566/000000000000/login-queue',
    MaxNumberOfMessages=10
)

messages = response.get('Messages', [])
for message in messages:
    body = json.loads(message['Body'])
    user_id = body.get('user_id')
    device_type = body.get('device_type')
    masked_ip = mask_pii(body.get('ip'))
    masked_device_id = mask_pii(body.get('device_id'))
    locale = body.get('locale')
    app_version = body.get('app_version')
    create_date = datetime.strptime(body.get('create_date'), '%Y-%m-%d').date()

    # Insert into Postgres
    insert_query = sql.SQL("""
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """)
    cur.execute(insert_query, (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date))

# Commit and close
conn.commit()
cur.close()
conn.close()
