import os

import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


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


