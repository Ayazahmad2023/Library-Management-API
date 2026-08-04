from fastapi import FastAPI
from app.routers import authors, books, users
from app.database import Base, engine
from app import models
from app.routers import authors, books
from app.routers import authors, books, users, borrow

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    description="A learning project: users, authors, books, and borrow records.",
    version="0.1.0",
)


@app.get("/")
def read_root():
    """A simple health-check endpoint — good for confirming the server is alive."""
    return {"message": "Library Management API is running. Visit /docs to try it out."}


app.include_router(authors.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(borrow.router)