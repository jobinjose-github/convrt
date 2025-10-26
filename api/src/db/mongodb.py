import ssl
from config.config_loader import load_config
from pymongo import MongoClient
from pymongo.server_api import ServerApi

configs = load_config()

MONGO_URI = configs["database"]["db_url"]

client = MongoClient(
    MONGO_URI,
    server_api=ServerApi('1'),
    tls=configs["database"]["db_tls"],
    tlsAllowInvalidCertificates=configs["database"]["db_tls_allow_invalid_cert"]
)

try:
    client.admin.command('ping')
    print("✅ You successfully connected to MongoDB!")
except Exception as e:
    print("❌ Connection error:", e)
    
db = client[configs["database"]["db_name"]]

def get_database():
    return db
