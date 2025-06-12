import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI
from auth import authrouter
from todo_CRUD import todo_router
from todo_filter import todo_filter_router

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="password",
    database="todo",
    cursor_factory=RealDictCursor
    )

cursor = conn.cursor()

app = FastAPI()

app.include_router(authrouter)
app.include_router(todo_router)
app.include_router(todo_filter_router)
