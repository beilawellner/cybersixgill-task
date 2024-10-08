import os
from dotenv import load_dotenv
import logging
import logging.config

load_dotenv()

BUCKET_NAME = 'cybersixgill-core-team'
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')


import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("app.log"),
                            logging.StreamHandler()
                        ])


logger = logging.getLogger(__name__)
logger.info("Logging is configured.")
