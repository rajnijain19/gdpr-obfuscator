import csv
import io
import os

import boto3
import pandas as pd
import pytest
from moto import mock_aws

from src.utils import get_file_from_s3, obfuscate_data


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


class TestGetFileFromS3:
    def test_raises_exception_when_path_prefix_not_correct(self, s3_client):
        """raise exception when filepath doesn't start with s3://"""
        with pytest.raises(Exception):
            get_file_from_s3(s3_client, "my-ingestion-bucket/new_data/file1.csv")

    def test_raises_exception_when_filepath_is_not_correct(self, s3_client):
        """raise ValueError when filepath is not correct"""
        with pytest.raises(Exception):
            get_file_from_s3(s3_client, "s3://my-ingestion-bucket")

    def test_raises_exception_when_file_format_is_not_csv(self, s3_client):
        """raises exception when file format is other than csv"""
        with pytest.raises(Exception):
            get_file_from_s3(s3_client, "s3://my-ingestion-bucket/new_data/file1.abc")

    def test_raises_exception_when_object_not_found(self, s3_client):
        """raises exception when object is not found on s3 location"""
        with pytest.raises(Exception):
            get_file_from_s3(s3_client, "s3://my-ingestion-bucket/new_data/file1.csv")

    def test_returns_correct_data(self, s3_client):
        """returns correct data when_everything_is fine_with_the_request"""
        buffer = io.StringIO(newline="")
        writer = csv.writer(buffer)
        writer.writerow(["id", "name", "age", "email"])
        data = [
            [1, "A", 20, "a@xyz.com"],
            [2, "B", 23, "b@xyz.com"],
            [3, "C", 25, "c@xyz.com"],
        ]
        writer.writerows(data)
        expected = (
            "id,name,age,email\n"
            "1,A,20,a@xyz.com\n"
            "2,B,23,b@xyz.com\n"
            "3,C,25,c@xyz.com"
        )
        s3_client.put_object(
            Bucket="my-ingestion-bucket",
            Key="new_data/file1.csv",
            Body=buffer.getvalue(),
        )
        data = get_file_from_s3(
            s3_client, "s3://my-ingestion-bucket/new_data/file1.csv"
        )
        assert data.replace("\r", "").replace("\n", "") == expected.replace(
            "\r", ""
        ).replace("\n", "")


class TestObfuscateData:
    """anonymises data for requested fields and returns processed data"""

    def test_anonymises_data_for_fields_in_the_csv_file(self):
        expected = """id,name,age,email1,***,20,***2,***,23,***3,***,25,***"""
        buffer = io.StringIO(newline="")
        writer = csv.writer(buffer)
        writer.writerow(["id", "name", "age", "email"])
        data = [
            [1, "A", 20, "a@xyz.com"],
            [2, "B", 23, "b@xyz.com"],
            [3, "C", 25, "c@xyz.com"],
        ]
        writer.writerows(data)
        buffer.seek(0)
        df = pd.read_csv(buffer)
        result = obfuscate_data(df, ["name", "email"]).to_csv(index=False)
        assert result.replace("\r", "").replace("\n", "") == expected.replace(
            "\r", ""
        ).replace("\n", "")

    def test_returns_unchanged_data_for_empty_list_of_fields(self):
        """returns unchanged data when no fields supplied to be obfuscated"""
        buffer = io.StringIO(newline="")
        writer = csv.writer(buffer)
        writer.writerow(["id", "name", "age", "email"])
        data = [
            [1, "A", 20, "a@xyz.com"],
            [2, "B", 23, "b@xyz.com"],
            [3, "C", 25, "c@xyz.com"],
        ]
        writer.writerows(data)
        buffer.seek(0)
        df = pd.read_csv(buffer)
        result = obfuscate_data(df, []).to_csv(index=False)
        buffer.seek(0)
        assert result.replace("\r", "").replace("\n", "") == buffer.read().replace(
            "\r", ""
        ).replace("\n", "")
