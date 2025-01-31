
from pymongo.mongo_client import MongoClient
from decouple import config

uri = config("DATABASE_URI")

client = MongoClient(uri)

db = client[config("DATABASE_NAME")]

async def get_database(self, database):
    return db


def init_db():
    db.create_collection("user", check_exists=True)
    db.create_collection("task", check_exists=True)
    db.create_collection("project", check_exists=True)
    db.usuarios.create_index("email", unique=True)
    print("Banco de dados criado com sucesso")
