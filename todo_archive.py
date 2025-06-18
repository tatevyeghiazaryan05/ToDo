from fastapi import APIRouter, Depends, HTTPException

import main
from security import get_current_user

todo_archive_router = APIRouter(tags=["Todo archive"])


@todo_archive_router.get("/api/todo/archive/{todo_id}")
def archive_todo(todo_id: int, token=Depends(get_current_user)):
    try:
        main.cursor.execute("""
            INSERT INTO archivetodo 
            (todo_id, user_id, title, description, category, due_date, status, updated_at, created_at)
            SELECT id, user_id, title, description, category, due_date, status, updated_at, created_at
            FROM todo WHERE id = %s
        """, (todo_id,))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error archiving todo: {str(e)}")

    try:
        main.cursor.execute("DELETE FROM todo WHERE id = %s", (todo_id,))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting todo: {str(e)}")

    try:
        main.conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error committing changes: {str(e)}")

    return {"message": "Todo archived successfully."}
