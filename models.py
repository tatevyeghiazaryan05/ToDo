from sqlalchemy import Column, String, Integer, text, TIMESTAMP,ForeignKey, Date, Boolean

from database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)
    due_date = Column(Date)
    status = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
