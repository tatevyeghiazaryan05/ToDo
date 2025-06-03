from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException

import main
from security import get_current_user

todo_router = APIRouter()


class UpdateTodo(BaseModel):
    field: str
    value: str


@todo_router.put("/api/todo/update")
def update_todo(data: UpdateTodo, token: dict = Depends(get_current_user)):
    user_id = token["id"]
    allowed_fields = ["title", "description", "category", "status"]

    if data.field not in allowed_fields:
        raise HTTPException(status_code=400, detail="Invalid field name")

    try:
        main.cursor.execute(
            f"UPDATE todo SET {data.field} = %s WHERE user_id = %s",
            (data.value, user_id)
        )
        main.conn.commit()
        return f"{data.field} updated successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
