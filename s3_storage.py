import io
import boto3
import json
import pandas as pd
import logging
logger = logging.getLogger(__name__)
from config import BUCKET_NAME, ACCESS_KEY, SECRET_ACCESS_KEY

class S3Client:  
    """
    A class to connect to S3 and perform file operations.
    """

    def __init__(self):
        self.aws_access_key_id = ACCESS_KEY
        self.aws_secret_access_key = SECRET_ACCESS_KEY
        self.s3_client = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)
        logger.info("S3 client is initialized.")


    def list_objects(self):
        try:
            logger.info("Listing objects in S3 bucket.")
            paginator = self.s3_client.get_paginator('list_objects_v2')
            object_keys = []
            for page in paginator.paginate(Bucket=BUCKET_NAME):
                for content in page.get('Contents', []):
                    object_keys.append(content['Key'])
            logger.info(f"Found {len(object_keys)} objects in the S3 bucket.")
            return object_keys
        except Exception as e:
            logger.error("Error while listing objects in S3 bucket.")
            raise e
    
        
    def get_file_content(self, file_path, extension):
        try:
            logger.info(f"Reading file: {file_path}")
            # Download the file
            obj = self.s3_client.get_object(Bucket=BUCKET_NAME, Key=file_path)
            file_content = obj['Body'].read().decode('utf-8')
            
            # Determine the file extension and process accordingly
            if extension == '.json':
                data = json.loads(file_content)
                return pd.json_normalize(data, record_path=['credentials'], errors='ignore')
            elif extension == '.csv':
                return pd.read_csv(io.StringIO(file_content))
            elif extension == '.sql':
                # SQL files are raw content and would need custom parsing
                # Here, we just return the raw content
                return file_content
            else:
                raise ValueError("Unsupported file extension")
        
        except Exception as e:
            logger.error(f"Error while reading file: {file_path}")
            raise e
