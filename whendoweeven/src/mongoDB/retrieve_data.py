


def test_connection():

    load_dotenv(dotenv_path="../../.env")
    PASSWORD: str = os.getenv("PASSWORD")

    uri = f"mongodb+srv://vs9589:{PASSWORD}@cluster0.2gslk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


def connect_to_DB():
    pass


if __name__ == "__main__":
    test_connection()