import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from auth import authrouter
from todo_CRUD import todo_router
from todo_filter import todo_filter_router
from todo_archive import todo_archive_router

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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authrouter)
app.include_router(todo_router)
app.include_router(todo_filter_router)
app.include_router(todo_archive_router)
