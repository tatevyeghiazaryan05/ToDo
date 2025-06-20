from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Form, status

import main
from security import get_current_user
from Todo_Update_Schema import TodoUpdateSchema

todo_router = APIRouter()


@todo_router.post("/api/todo/add/todo")
def add_todo(
        title: str = Form(...),
        description: str = Form(...),
        category: str = Form(...),
        due_date: date = Form(...),
        token=Depends(get_current_user)

):
    user_id = token["id"]
    try:
        main.cursor.execute(
            """INSERT INTO todo (user_id, category, title, description, due_date)
             VALUES (%s, %s, %s, %s, %s)""",
            (user_id, category, title, description, due_date)
        )
        main.conn.commit()
    except Exception:
        raise HTTPException(status_code=500, detail="Server error during todo addition")


@todo_router.get("/api/todo/get/all/todo")
def get_todo(token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id=%s",
                            (user_id,))
    except Exception:
        raise HTTPException(status_code=500, detail="Error fetching todo info")

    try:
        todos = main.cursor.fetchall()

    except Exception:
        raise HTTPException(status_code=500, detail="Database fetch error")

    if todos is None:
        raise HTTPException(status_code=404, detail="No ToDo found in this date range")
    else:
        return todos


@todo_router.put("/api/todo/change/{todo_id}")
def update_todo(updates: TodoUpdateSchema, todo_id: int, token=Depends(get_current_user)):
    try:
        main.cursor.execute("""SELECT * FROM todo WHERE id=%s""", (todo_id,))
    except Exception:
        raise HTTPException(status_code=500, detail="Error fetching todo")

    try:
        todo = main.cursor.fetchone()
    except Exception:
        raise HTTPException(status_code=500, detail="Database fetch error")

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found!"
        )

    try:
        todo = dict(todo)
        update_data = updates.model_dump()

        for key, value in update_data.items():
            if value is None:
                setattr(updates, key, todo[key])

        updated_at = datetime.now()

        main.cursor.execute("""
            UPDATE todo SET 
                title=%s, description=%s, category=%s, status=%s, due_date=%s, updated_at=%s
            WHERE id=%s
            """,
            (updates.title, updates.description, updates.category, updates.status,
             updates.due_date, updated_at, todo_id)
        )
        main.conn.commit()
    except Exception:
        raise HTTPException(status_code=500, detail="Error updating todo")


@todo_router.delete("/api/todo/delete/todo")
def delete_todo(token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("DELETE FROM todo WHERE user_id=%s",
                            (user_id,))
        main.conn.commit()
    except Exception:
        raise HTTPException(status_code=500, detail="Server error during todo deletion")
