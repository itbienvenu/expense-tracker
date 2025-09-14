from fastapi import FastAPI
from database.dbs import engine, Base
import database.models

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/")
def main():
    return {"message":"Home route"}
