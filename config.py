import os
from dotenv import load_dotenv

load_dotenv()

# Google Cloud settings
PROJECT_ID = os.getenv('PROJECT_ID')
SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID')

# MongoDB settings
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DB = os.getenv('MONGODB_DB')
POSTS_COLLECTION = os.getenv('POSTS_COLLECTION', 'posts')

# BERTopic settings
BERTOPIC_MODEL_PATH = os.getenv('BERTOPIC_MODEL_PATH', 'model') 