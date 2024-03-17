import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    MAIL_KEY = os.getenv('MAIL_KEY')
    Email=os.getenv('Email')
    #bunny
    STORAGE_API_KEY = os.getenv('storage_api_key')
    STORAGE_ZONE_NAME = os.getenv('storage_zone_name')
    STORAGE_CDN = os.getenv('Storage_cdn')
