import os
import re
from email_validator import validate_email, EmailNotValidError
import pandas as pd
from s3_storage import S3Client
import logging
from config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def create_df_from_sql(file_content):
    try:
        logger.info("Creating DataFrame from SQL file.")
        pattern = re.compile(r"\('([^']*)',[^,]*,\s*'([^']*)',")
        df = pattern.findall(file_content)
        return df
    except Exception as e:
        raise e


def parse_file(df, file_key, extension):
    try:
        logger.info(f"Parsing file: {file_key}")
        if extension == '.sql':
            df = create_df_from_sql(df)
        df = pd.DataFrame(df, columns=['email', 'password'])
        data = []
        if 'email' in df.columns:
            for _, row in df.iterrows():
                email = row.get('email')
                if pd.notna(email):
                    try:
                        if validate_email(email):
                            password = row.get('password', None)
                            data.append({'file': file_key, 'email': email, 'password': password})
                    except EmailNotValidError as e:
                        logger.info(f"Invalid email: {email}")
        result_df = pd.DataFrame(data)
        logger.info(f"Extracted {len(result_df)} records from the file.")
        return result_df
    except Exception as e:
        raise e
    

def save_to_csv(data, file_name='leaked_data.csv'):
    try:
        logger.info(f"Saving data to CSV: {file_name}")
        if not pd.io.common.file_exists(file_name):
            data.to_csv(file_name, index=False, mode='w', header=True)
        else:
            data.to_csv(file_name, index=False, mode='a', header=False)
    except Exception as e:
        raise e
    

def main():
    try:
        logger.info('Starting the main')
        s3_client = S3Client()
        file_list = s3_client.list_objects()
        
        for file_key in file_list:
            logger.info(f"Processing file: {file_key}")
            _, extension = os.path.splitext(file_key)
            file_content = s3_client.get_file_content(file_key, extension=extension)
            extracted_data = parse_file(file_content, file_key, extension=extension)
            save_to_csv(extracted_data)
        
        final_csv = pd.read_csv('leaked_data.csv')
        logger.info(f"Total records extracted: {len(final_csv)}")
        
        logger.info('Processing completed.')        
    
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
