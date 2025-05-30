from fastapi import APIRouter, Depends, HTTPException

import main
from security import get_current_user

todo_router = APIRouter()


@todo_router.put("/api/todo/change/todo/title/{new_title}")
def change_todo_title(new_title: str, token: Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("UPDATE todo SET title=%s WHERE user_id=%s",
                            (new_title,user_id))
        main.conn.commite()
        return {"message": "Todo title updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating todo title: {str(e)}")


@todo_router.put("/api/todo/change/todo/description/{new_description}")
def change_todo_description(new_description: str, token: Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("UPDATE todo SET description=%s WHERE user_id=%s",
                            (new_description, user_id))
        main.conn.commite()
        return {"message": "Todo description updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating todo title: {str(e)}")


@todo_router.put("/api/todo/change/todo/category/{new_category}")
def change_todo_category(new_category: str, token: Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("UPDATE todo SET category=%s WHERE user_id=%s",
                            (new_category, user_id))
        main.conn.commite()
        return {"message": "Todo category updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating todo title: {str(e)}")


@todo_router.put("/api/todo/change/todo/status/{new_status}")
def change_todo_status(new_status: str, token: Depends(get_current_user)):
    user_id = token["id"]
    try:
        main.cursor.execute("UPDATE todo SET status=%s WHERE user_id=%s",
                            (new_status, user_id))
        main.conn.commite()
        return {"message": "Todo status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating todo title: {str(e)}")
