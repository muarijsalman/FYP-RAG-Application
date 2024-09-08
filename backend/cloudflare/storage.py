import boto3
from fastapi import UploadFile
from utils import get_aws_access_id, get_aws_bucket_name, get_aws_secret_key, get_aws_endpoint_url
from tempfile import NamedTemporaryFile

class CloudflareR2:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=get_aws_access_id(),
            aws_secret_access_key=get_aws_secret_key(),
            endpoint_url=get_aws_endpoint_url()
        )
        self.bucket_name = get_aws_bucket_name()
    
    def upload_document(self, _file: UploadFile, file_path: str):
        try:
            with NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(_file.file.read())
            self.client.upload_file(
                Filename=temp_file.name, 
                Bucket=self.bucket_name, 
                Key=file_path
            )
            temp_file.close()
            return True
        except Exception as e:
            print(e)
            return False