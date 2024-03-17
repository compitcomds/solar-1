from BunnyCDN.CDN import CDN
from BunnyCDN.Storage import Storage
from config import Config

storage_api_key=Config.STORAGE_API_KEY
storage_api_key=Config.STORAGE_API_KEY
storage_zone_name=Config.STORAGE_ZONE_NAME
storage_zone_name="stocksales"

obj_storage = Storage(storage_api_key,storage_zone_name)
obj_cdn = CDN(Config.STORAGE_CDN)