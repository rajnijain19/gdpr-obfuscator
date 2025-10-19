import json
import os
import time

import boto3
import pytest
from moto import mock_aws

from src.obfuscator import obfuscator


@pytest.fixture(scope="module")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="module")
def mocked_aws(aws_credentials):
    """Mock all AWS interactions."""
    with mock_aws():
        yield


@pytest.fixture(scope="module")
def s3_client(mocked_aws):
    """Mock boto3 client"""
    s3_client = boto3.client("s3")
    s3_client.create_bucket(Bucket="my-ingestion-bucket")
    yield s3_client


def test_obfuscation_process_handles_upto_1MB_file_within_a_minute(s3_client):
    """tests the performance criteria that this tool handles files of upto
    1MB within a runtime of less than 1 minute. It reads data from local
    test file of size upto 1MB, does processing on it, measures that
    process finishes within 1 minute
    """
    try:
        with open("data/Sample_Employees.csv", "rb") as f:
            contents = f.read()
    except Exception:
        raise Exception("Local test file data/Sample_Employees.csv not found.")
    size = len(contents)
    assert size <= 1000000, "Test file larger than 1MB"
    bucket_name = "my-ingestion-bucket"
    key = "new_data/file1.csv"
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=contents)
    input = {
        "file_to_obfuscate": f"s3://{bucket_name}/{key}",
        "pii_fields": ["fullname", "email", "phone"],
    }
    input_json = json.dumps(input)
    start_time = time.perf_counter()
    result = obfuscator(input_json)
    result.read()
    end_time = time.perf_counter()
    runtime = end_time - start_time
    assert runtime < 60
