# GDPR obfuscator


python script/load_sample_data.py
python src/obfuscator.py '{"file_to_obfuscate": "s3://my-ingestion-bucket-001/new_data/file1.csv","pii_fields": ["fullname", "email","phone"]}'
pytest test/integration/test_obfuscator_performance.py 
pytest test/unit/test_obfuscator.py
pytest test/unit/test_utils.py