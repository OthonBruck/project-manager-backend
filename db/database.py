
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

uri = config("DATABASE_URI")

client = AsyncIOMotorClient(uri)

db = client[config("DATABASE_NAME")]

def get_database():
    return db


def init_db():
    #db.create_collection("user", check_exists=True)
    #db.create_collection("task", check_exists=True)
    #db.create_collection("project", check_exists=True)
    #db.usuarios.create_index("email", unique=True)
    print("Banco de dados criado com sucesso")
