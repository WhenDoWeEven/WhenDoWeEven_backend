from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv



def connect_to_mongoDB() -> MongoClient:

    load_dotenv(dotenv_path="../../.env")
    PASSWORD: str = os.getenv("PASSWORD")

    uri = f"mongodb+srv://vs9589:{PASSWORD}@cluster0.2gslk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)


if __name__ == "__main__":
    client: MongoClient = connect_to_mongoDB()

    databases: list[str] = client.list_database_names()

    print(databases)