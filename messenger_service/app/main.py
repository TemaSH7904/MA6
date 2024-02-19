import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from database import database as database
from database.database import Message
from model.message import MessageModel
from datetime import datetime

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
author = ""


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}

@app.post("/login", status_code=status.HTTP_200_OK)
async def login(name: str):
    global author
    author = name
    return f"You logged in as {author}"

@app.post("/send_message")
async def send_message(receiver_name: str, text: str, db: db_dependency):
    message_db = Message(sender_name=author,
                         receiver_name=receiver_name,
                         datetime=datetime.now(),
                         text=text)
    try:
        db.add(message_db)
        db.commit()
        db.refresh(message_db)
        return "Success"
    except Exception as e:
        return "Cant add message"

@app.get("/get_messages_with_user")
async def get_messages_from_user(username: str, db: db_dependency):
    try:
        result = db.query(Message).filter(
            or_(
                and_(Message.receiver_name == author, Message.sender_name == username),
                and_(Message.receiver_name == username, Message.sender_name == author)
            )
        ).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Messages not found")

@app.get("/get_messages_from")
async def get_messages_from_user(username: str, db: db_dependency):
    try:
        result = db.query(Message).filter(
            and_(
                Message.receiver_name == author,
                Message.sender_name == username
            )
        ).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Messages not found")

@app.get("/get_messages_to")
async def get_messages_to_user(username: str, db: db_dependency):
    try:
        result = db.query(Message).filter(
            and_(
                Message.receiver_name == username,
                Message.sender_name == author
            )
        ).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Messages not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))