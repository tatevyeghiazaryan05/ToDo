import os

import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI
from auth import authrouter
from User_ToDo_service import user_add_todo_service
from User_ToDo_service import user_change_todo_service

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
app.include_router(user_add_todo_service.todo_router)
app.include_router(user_change_todo_service.todo_router)
