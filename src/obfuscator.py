import json
import sys
from io import BytesIO, StringIO

import boto3
import pandas as pd

from src.utils import get_file_from_s3, obfuscate_data


def obfuscator(input):
    """
    function to read file from AWS S3, obfuscate sensitive information
    and return obfuscated file back to calling program.

    Parameters:
    input (str): A JSON formatted string containing filepath and fields to be
    obfuscated.

    Returns:
    io.BytesIO: A file like object containing generated binary
    data. Sensitive fields are obfuscated, non-sentivite fields are intact.
    """
    s3_client = boto3.client("s3")
    input_dict = json.loads(input)
    filepath = input_dict["file_to_obfuscate"].strip()
    data = get_file_from_s3(s3_client, filepath)
    df = pd.read_csv(StringIO(data))
    proc_df = obfuscate_data(df, input_dict["pii_fields"])
    proc_data = proc_df.to_csv(index=False).encode("utf-8")
    return BytesIO(proc_data)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Error - Incorrect number of arguments. The program must to be "
            "called with a JSON string containing a filename and fields to "
            "be obfuscated as in the example below:"
        )
        print(
            '{"file_to_obfuscate": "s3://your-bucket-name/filepath",'
            '"pii_fields": ["name", "email"]}'
        )
    else:
        print(obfuscator(sys.argv[1]).read().decode("utf-8"))
