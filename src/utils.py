from botocore.exceptions import ClientError


def get_file_from_s3(s3_client, file_path):
    """
    This fuction gets requested file from AWS S3

    Parameters:
    s3_client (botocore.client.S3): A boto3 S3 client
    file_path (str): Path of file on S3

    Returns:
    str: contents of S3 object converted to text

    Raises:
    Raises:
        Exception: If the file path does not start with 's3://'.
        ValueError: If the file path is incorrect.
        Exception: If the file format is not CSV.
        Exception: If the specified file does not exist in the bucket.
        ClientError: For other errors that might occur when fetching
        object from S3.

    """
    if not file_path.startswith("s3://"):
        raise Exception("File path must start with s3://")
    try:
        bucket_name, obj_key = file_path.removeprefix("s3://").split("/", 1)
    except ValueError as e:
        raise ValueError("File path is not correct") from e
    if not obj_key.strip().lower().endswith(".csv"):
        raise Exception("Unsupported file format. Only csv is supported.")
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=obj_key)
    except ClientError as c:
        if c.response["Error"]["Code"] == "NoSuchKey":
            raise Exception("There is no such file in the bucket")
        else:
            raise c
    return response["Body"].read().decode("utf-8")


def obfuscate_data(df, fields):
    """
    This function obfuscates sensitive fields.

    Parameters:
    df (pd.Dataframe): Pandas Dataframe containing sensitive fields
    fields (list): List of sensitive fields to be obfuscated

    Returns:
    pd.Dataframe: Pandas Dataframe containing obfuscated sensitive fields
    leaving other intact.
    """
    for field in fields:
        if field in df.columns:
            df[field] = "***"
    return df
