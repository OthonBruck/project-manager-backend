from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import init_db
from api.routers import user_router
from decouple import config
from contextlib import asynccontextmanager


# Eventos de inicialização e encerramento
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    init_db()
    yield
    print("Ending application...")
    
# Criação da aplicação
app = FastAPI(
    title=config("PROJECT_NAME"),
    version=config("VERSION"),
    description="API build for managing collaborative projects",
    lifespan=lifespan
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config("ALLOWED_ORIGINS"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão de routers
app.include_router(user_router, prefix="/users", tags=["Users"])
#app.include_router(project_router, prefix="/projects", tags=["Projects"])
#app.include_router(task_router, prefix="/tasks", tags=["Tasks"])

# Apenas para execução local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
