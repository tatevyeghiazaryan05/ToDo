# from pydantic import BaseModel
# from datetime import date
#
# from typing import Optional
#
#
# from fastapi import APIRouter, Depends, HTTPException, status
#
# import main
# from security import get_current_user
#
# todo_router = APIRouter()
#
#
# class UpdateTodo(BaseModel):
#     title: Optional[str] = None
#     description: Optional[str] = None
#     category: Optional[str] = None
#     status: Optional[str] = None
#     due_date: Optional[date] = None
#
#
# @todo_router.put("/api/todo/update/{todo_id}")
# def update_todo(todo_id: int, data: UpdateTodo, token: dict = Depends(get_current_user)):
#     user_id = token.get("id")
#
#     data_dict = data.__dict__
#     fields_to_update = {}
#     for key in data_dict:
#         if data_dict[key] is not None:
#             fields_to_update[key] = data_dict[key]
#
#     if not fields_to_update:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#
#     fields_to_update = list(fields_to_update.items())
#     print(fields_to_update)
# # [("description", "new descp"), ("due_date", "2025-06-12")]
#     upd_fields = ""
#     upd_values = ""
#     for t in fields_to_update:
#         upd_fields = upd_fields + t[0] + "%s,"
#         upd_values = upd_values + str(t[1]) + " "
#
#     print(upd_fields)
#     try:
#         main.cursor.execute(
#             f"UPDATE todo SET {upd_fields[:-1]} WHERE user_id = %s AND id=%s",
#             (*upd_values.split(" "), user_id, todo_id)
#         )
#         main.conn.commit()
#         return f"{data.field} updated successfully"
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


from fastapi import APIRouter, Depends, HTTPException

import main
from security import get_current_user
from Todo_Update_Schema import TodoUpdateSchema

todo_router = APIRouter()


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

# todo  write schema in other file +
