from fastapi import FastAPI
from database.dbs import engine, Base
import database.models
from fastapi.middleware.cors import CORSMiddleware 
from routers import users_router, transactions_category_router, reports_router

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)
app.include_router(users_router.router)
app.include_router(transactions_category_router.router)
app.include_router(reports_router.router)

@app.get("/")
def main():
    return {"message":"Home route"}
