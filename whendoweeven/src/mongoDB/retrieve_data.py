from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv


load_dotenv()
PASSWORD: str = os.getenv("PASSWORD")
uri = "mongodb+srv://vs9589:{PASSWORD}@cluster0.2gslk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection

client.admin.command('ping')
print("Pinged your deployment. You successfully connected to MongoDB!")



def connect_to_DB():
    pass