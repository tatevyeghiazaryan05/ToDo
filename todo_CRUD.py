from datetime import date


from fastapi import APIRouter, Depends, HTTPException, Form

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

        return {"message": "ToDo  added successfully"}

    except Exception:
        raise HTTPException(status_code=500, detail="Server error during todo addition")


@todo_router.get("/api/todo/get/all/todo")
def get_todo(token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("SELECT * FROM todo where user_id=%s",
                            (user_id,))
        main.cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo info: {str(e)}")


@todo_router.put("/api/todo/change")
def update_todo(updates: TodoUpdateSchema, token=Depends(get_current_user)):
    user_id = token["id"]

    try:
        if updates.title is not None:
            main.cursor.execute("UPDATE todo SET title=%s WHERE user_id=%s", (updates.title, user_id))
            main.conn.commit()

        if updates.description is not None:
            main.cursor.execute("UPDATE todo SET description=%s WHERE user_id=%s", (updates.description, user_id))
            main.conn.commit()

        if updates.category is not None:
            main.cursor.execute("UPDATE todo SET category=%s WHERE user_id=%s", (updates.category, user_id))
            main.conn.commit()

        if updates.status is not None:
            main.cursor.execute("UPDATE todo SET status=%s WHERE user_id=%s", (updates.status, user_id))
            main.conn.commit()

        if updates.due_date is not None:
            main.cursor.execute("UPDATE todo SET due_date=%s WHERE user_id=%s", (updates.due_date, user_id))
            main.conn.commit()

        return "Todo updated successfully!!"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@todo_router.delete("/api/todo/delete/todo")
def delete_todo(token=Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("DELETE FROM todo WHERE user_id=%s",
                            (user_id,))
        main.conn.commit()

        return {"message": "ToDo  deleted successfully"}

    except Exception:
        raise HTTPException(status_code=500, detail="Server error during todo deletion")
