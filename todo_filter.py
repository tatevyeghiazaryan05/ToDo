from datetime import date

from fastapi import APIRouter, Depends, HTTPException

import main
from security import get_current_user

todo_filter_router = APIRouter(prefix="/api/todo/get", tags=["Todo Filter"])


@todo_filter_router.get("/all/unfinished/todo/")
def get_unfinished_todo(token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND status=%s",
                            (user_id, "False"))
        main.cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo info: {str(e)}")


@todo_filter_router.get("/by/title/{title}")
def get_todo_by_title(title: str, token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND title=%s",
                            (user_id, title))
        main.cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo info: {str(e)}")


@todo_filter_router.get("/all/by/category/{category}")
def get_todo_by_category(category: str, token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND category=%s",
                            (user_id, category))
        main.cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo info: {str(e)}")


@todo_filter_router.get("/all/by/due_date/{deadline}")# todo write date  range
def get_todo_by_due_date(deadline: date, token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND deadline=%s",
                            (user_id, deadline))
        main.cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo info: {str(e)}")
