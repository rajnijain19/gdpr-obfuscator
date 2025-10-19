import io

import boto3
from botocore.exceptions import ClientError


def load_sample_on_s3():
    """
    This function will upload a local file containing test data upto 1 MB
    onto S3 bucket.

    Raises:
    ClientError: If S3 service returns an error while uploading the file.
    Exception: For any other enexpected errors.
    """
    s3_client = boto3.client("s3")
    bucket_name = "my-ingestion-bucket-001"
    with open("data/Sample_Employees.csv", "r") as f:
        data = f.read()
        data = io.BytesIO(data.encode("utf-8"))
    try:
        s3_client.put_object(Bucket=bucket_name, Key="new_data/file1.csv", Body=data)
        print("Object upload request successfully completed.")
    except (ClientError, Exception) as e:
        print(f"Object Upload request failed. Details: {e}")


if __name__ == "__main__":
    load_sample_on_s3()
