from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import users

#to create tables in PostgreSQL
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register the /users endpoint
app.include_router(users.router)
