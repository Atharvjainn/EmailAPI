from fastapi import FastAPI
from app.api.email_routes import router as email_router

app = FastAPI()

app.include_router(email_router)

