import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Todo, Users
from email_service import send_verification_email


def check_reminders():
    while True:
        db: Session = SessionLocal()
        now = datetime.now()

        try:
            tasks = db.query(Todo).filter(
                Todo.archived == None,
                Todo.status == None,
                Todo.due_date != None
            ).all()
            print(tasks)

            for task in tasks:
                print(task)
                time_left = task.due_date - now.date()

                if timedelta(days=0) <= time_left <= timedelta(days=1):
                    user = db.query(Users).filter_by(id=task.user_id).first()
                    if user and user.email:
                        message = (
                            f"🔔 Reminder\n\n"
                            f"Dear {user.name},\n"
                            f"Your task '{task.title}' is due on {task.due_date}.\n"
                            f"Please don't forget to complete it on time."
                        )
                        send_verification_email(user.email, message)
                        print(f"✅ Reminder sent to {user.email} for task '{task.title}'")

        except Exception as e:
            print(f"❌ Error: {e}")

        finally:
            db.close()

        print("⏳ Waiting 5 minutes for next check...")
        time.sleep(300)

check_reminders()
