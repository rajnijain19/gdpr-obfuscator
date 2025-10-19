import json
from io import BytesIO, StringIO
from unittest.mock import patch

import pandas as pd

from src.obfuscator import obfuscator


def test_obfuscator():
    """
    Test that obfuscator returns expected output which is compatible with
    boto3 Put object API by asserting that it is of type BytesIO
    """
    input = {
        "file_to_obfuscate": "s3://my-ingestion-bucket/new_data/file1.csv",
        "pii_fields": ["name", "email"],
    }
    input_json = json.dumps(input)
    data = """
    id,name,age,email\n1,A,20,a@xyz.com\n2,B,23,b@xyz.com\n3,C,25,c@xyz.com
    """
    proc_data = """
    id,name,age,email\n1,***,20,***\n2,***,23,***\n3,***,25,***
    """
    with patch("src.obfuscator.get_file_from_s3", return_value=data), patch(
        "src.obfuscator.obfuscate_data", return_value=pd.read_csv(StringIO(proc_data))
    ):
        result = obfuscator(input_json)
        assert isinstance(result, BytesIO)
        assert result.getvalue().decode("utf-8").strip() == proc_data.strip()
