import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated

from sqlalchemy.orm import Session

from database import database as database
from database.database import Message

from model.message import MessageModel

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/get_messages")
async def get_messages(db: db_dependency):
    try:
        result = db.query(Message).limit(100).all()
        return result
    except Exception as e:
        return "Cant access database!"


@app.get("/get_message_by_sender")
async def get_message_by_sender(name: str, db: db_dependency):
    try:
        result = db.query(Message).filter(Message.sender_name == name).first()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return result

@app.get("/get_message_by_reciever")
async def get_message_by_sender(name: str, db: db_dependency):
    try:
        result = db.query(Message).filter(Message.receiver_name == name).first()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return result

@app.delete("/delete_message")
async def delete_message(message_id: int, db: db_dependency):
    try:
        message = db.query(Message).filter(Message.id == message_id).first()
        db.delete(message)
        return "Success"
    except Exception as e:
        return "Cant find message"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
