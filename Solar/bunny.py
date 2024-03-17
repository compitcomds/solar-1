from BunnyCDN.CDN import CDN
from BunnyCDN.Storage import Storage
from config import Config

storage_api_key=Config.STORAGE_API_KEY
storage_api_key="7ac93fd8-09f9-4a9f-acc6c3515889-6e83-44d0"
storage_zone_name=Config.STORAGE_ZONE_NAME

obj_storage = Storage(storage_api_key,storage_zone_name)
obj_cdn = CDN(Config.STORAGE_CDN)