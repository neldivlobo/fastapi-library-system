from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import users, books, borrows



#to create tables in PostgreSQL
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register the /users endpoint
app.include_router(users.router)
app.include_router(books.router)
app.include_router(borrows.router)


