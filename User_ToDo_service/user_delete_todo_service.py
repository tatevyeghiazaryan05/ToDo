from fastapi import APIRouter, Depends, HTTPException

import main
from security import get_current_user


todo_router = APIRouter()


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
