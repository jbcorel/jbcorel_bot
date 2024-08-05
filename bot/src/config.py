import os

class Config:
    TOKEN = os.getenv('TG_API_TOKEN')
    API_URL = os.getenv('API_URL')