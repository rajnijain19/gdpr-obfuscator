# GDPR obfuscator (Python)

The purpose of this project is to create an obfuscation tool to process data being ingested to AWS S3 and obfuscate personally identifiable information (PII) (like names, emails, phone numbers, address etc) in CSV files. The tool will be supplied with the S3 location of a file containing sensitive information, and the names of the affected fields. It will create a new file or byte stream object containing an exact copy of the input file but with the sensitive data replaced with obfuscated strings. The source code (obfuscator.py and utils.py) can be found in src folder. It test folder includes unit tests (unit/test_obfuscator.py and unit/test_utils.py) and integration performance tests (integration/test_obfuscator_performance.py).

# Setup Instructions
1. Clone the Repository

```bash
git clone https://github.com/rajnijain19/gdpr-obfuscator
```
2. Change directory to project folder
```bash
cd gdpr-obfuscator
```
3. Create and Activate Virtual Environment
```bash
python -m venv venv
```
#On Linux/macOS: 
```bash
source venv/bin/activate        
```
#On Windows (powershell): 
```bash
.\venv\Scripts\Activate.ps1
```
4. Install Dependencies
```bash
pip install -r requirements.txt
```
5. Set Python Path
#On Linux/macOS: 
```bash
export PYTHONPATH=$(pwd)
```
#On Windows (powershell): 
```bash
$env:PYTHONPATH = (Get-Location).Path
```
6. A command-line interface (CLI) designed for seamless integration with AWS S3.
 
# Running Tests

Unit Tests -> Run the following to verify utility and obfuscation functions:
```bash
pytest test/unit/test_utils.py
pytest test/unit/test_obfuscator.py
```
Integration Test (Local) -> Test performance(File up to 1 MB should be processed within 1 minute) using the local file data/Sample_Employees.csv:
```bash
pytest test/integration/test_obfuscator_performance.py
```
# Running end-to-end test from AWS CLI

1. Configure AWS CLI using following command:
```bash
aws configure
```
You will be prompted to enter AWS credentials:
```bash
AWS Access Key ID [None]: <your-access-key-id>
AWS Secret Access Key [None]: <your-secret-access-key>
Default region name [None]: <your-default-region> # e.g. eu-west-2
Default output format [None]: json
```
Verify AWS CLI has been configured as shown below:
```bash
aws sts get-caller-identity
```
2. This is an optional step that will upload local test file(upto 1MB) on S3 for end-to-end testing. Execute this step only if uploading test data is needed. An existing data file could also be used. To Upload local test data to S3, update the bucket_name variable in script/load_sample_data.py with your own bucket name, then run the script to create and upload a file (up to 1 MB) on S3 with filepath new_data/file1.csv as shown below:
```bash
python script/load_sample_data.py
```
3. Run Obfuscator from CLI by updating bucket name, filepath and PII fields as per your environment:
```bash
python src/obfuscator.py '{"file_to_obfuscate": "s3://<your-bucket-name>/<new_data/file1.csv>","pii_fields": ["fullname", "email","phone"]}'
```

