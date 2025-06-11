from datetime import date

from fastapi import APIRouter, Depends, HTTPException

import main
from security import get_current_user

todo_core_router = APIRouter()


@todo_core_router.get("/api/todo/get/all/unfinished/todo/")
def get_unfinished_todo(token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND status=%s",
                            (user_id, "False"))
        main.cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo info: {str(e)}")


@todo_core_router.get("/api/todo/get/all/todo/by/title/{title}")
def get_todo_by_title(title: str, token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND title=%s",
                            (user_id, title))
        main.cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo info: {str(e)}")


@todo_core_router.get("/api/todo/get/all/todo/by/description/{description}")
def get_todo_by_description(description: str, token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND description=%s",
                            (user_id, description))
        main.cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo info: {str(e)}")


@todo_core_router.get("/api/todo/get/all/todo/by/category/{category}")
def get_todo_by_category(category: str, token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND category=%s",
                            (user_id, category))
        main.cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo info: {str(e)}")


@todo_core_router.get("/api/todo/get/all/todo/by/due_date/{deadline}")
def get_todo_by_due_date(deadline: date, token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id = %s AND deadline=%s",
                            (user_id, deadline))
        main.cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo info: {str(e)}")
