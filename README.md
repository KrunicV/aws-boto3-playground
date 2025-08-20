# Boto3 Intro Demos

This repository contains hands-on demos and experiments with **Boto3**, the AWS SDK for Python.

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/KrunicV/aws-boto3-playground.git
cd aws-boto3-playground
```

### 2. Set up a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        #Linux/Mac
venv\Scripts\activate   # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Project Structure

- `boto3_intro/session_demo.py` -> Demonstrates boto3 sessions, clients, resources, error handling, and logging.
- `s3_manager/s3_manager.py` ->  S3 operations: buckets, objects, multipart uploads, versioning.
- (more demos will be added as I continue learning AWS + Boto3)

## Projects

### 1. Boto3 Session Demo
**Features**
- Create boto3 sessions and clients
- Resource usage
- Error handling with logging

**Usage**
```bash
python boto3_intro/session_demo.py

```

---

### 2. S3 Manager
**Features**
- Create and delete buckets (with cleanup)
- Upload, download, and delete files
- Multipart upload
- List object versions
- Logging and error handling

**Usage**

```python
from s3_manager.s3_manager import create_bucket, upload_file, list_versions

bucket_name = "my-test-bucket"
create_bucket(bucket_name)
upload_file(bucket_name, "local_file.txt", "remote_file.txt")
list_versions(bucket_name)
```

**Notes**
- AWS credentials must be configured
- Buckets must have unique names

---




















