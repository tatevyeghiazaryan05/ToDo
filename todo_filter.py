from datetime import date

from fastapi import APIRouter, Depends, HTTPException

import main
from security import get_current_user
from schemas import ToDoDateSchema

todo_filter_router = APIRouter(prefix="/api/todo/get", tags=["Todo Filter"])


@todo_filter_router.get("/all/unfinished/todo/")
def get_unfinished_todo(token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND status=%s",
                            (user_id, "False"))
    except Exception:
        raise HTTPException(status_code=500, detail="Database query error")

    try:
        todos = main.cursor.fetchall()
    except Exception:
        raise HTTPException(status_code=500, detail="Database fetch error")

    if todos is None:
        raise HTTPException(status_code=404, detail="No ToDo found in this date range")


@todo_filter_router.get("/by/title/{title}")
def get_todo_by_title(title: str, token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND title=%s",
                            (user_id, title))
    except Exception:
        raise HTTPException(status_code=500, detail="Database query error")

    try:
        todo = main.cursor.fetchone()
    except Exception:
        raise HTTPException(status_code=500, detail="Database fetch error")

    if todo is None:
        raise HTTPException(status_code=404, detail="No ToDo found in this date range")


@todo_filter_router.get("/all/by/category/{category}")
def get_todo_by_category(category: str, token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND category=%s",
                            (user_id, category))
    except Exception:
        raise HTTPException(status_code=500, detail="Database query error")

    try:
        todos = main.cursor.fetchall()
    except Exception:
        raise HTTPException(status_code=500, detail="Database fetch error")

    if todos is None:
        raise HTTPException(status_code=404, detail="No ToDo found in this date range")


@todo_filter_router.get("/all/by/due_date/{deadline}")
def get_todo_by_due_date(date_data: ToDoDateSchema, token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where "
                            "user_id = %s AND deadline>=%s AND deadline<=%s",
                            (user_id, date_data.start_date, date_data.end_date))
    except Exception:
        raise HTTPException(status_code=500, detail="Database query error")

    try:
        todos = main.cursor.fetchall()
    except Exception:
        raise HTTPException(status_code=500, detail="Database fetch error")

    if todos is None:
        raise HTTPException(status_code=404, detail="No ToDo found in this date range")
