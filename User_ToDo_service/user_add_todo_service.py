from datetime import date


from fastapi import APIRouter, Depends, HTTPException, Form

import main
from security import get_current_user


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
            """INSERT INTO todo (user_id, category, title, description, due_date,)
             VALUES (%s, %s, %s, %s, %s)""",
            (user_id, category, title, description, due_date,)
        )
        main.conn.commit()

        return {"message": "ToDo  added successfully"}

    except Exception:
        raise HTTPException(status_code=500, detail="Server error during todo addition")
