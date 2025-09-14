from fastapi import FastAPI
from database.dbs import engine, Base
import database.models

from routers import users_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(users_router.router)

@app.get("/")
def main():
    return {"message":"Home route"}
