from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(title="Library API Mongo")
app.include_router(router)