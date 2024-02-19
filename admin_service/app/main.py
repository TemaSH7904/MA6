import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form
from typing import Annotated
from keycloak import KeycloakOpenID

from sqlalchemy.orm import Session

from database import database as database
from database.database import Message

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

# Данные для подключения к Keycloak
KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "Shalaev"
KEYCLOAK_REALM = "myRealm"
KEYCLOAK_CLIENT_SECRET = "zXkxCT1zhllUO1t6KqPC8qREQKklFNMM"

user_token = ""
keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

###########
#Prometheus
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

@app.post("/get_token")
async def get_token(username: str = Form(...), password: str = Form(...)):
    try:
        # Получение токена
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        global user_token
        user_token = token
        return token
    except Exception as e:
        print(e)  # Логирование для диагностики
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def check_user_roles():
    global user_token
    token = user_token
    try:
        userinfo = keycloak_openid.userinfo(token["access_token"])
        token_info = keycloak_openid.introspect(token["access_token"])
        if "myRole" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    if (check_user_roles()):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.get("/get_messages")
async def get_messages(db: db_dependency):
    if (check_user_roles()):
        try:
            result = db.query(Message).limit(100).all()
            return result
        except Exception as e:
            return "Cant access database!"
    else:
        return "Wrong JWT Token"


@app.get("/get_message_by_sender")
async def get_message_by_sender(name: str, db: db_dependency):
    if (check_user_roles()):
        try:
            result = db.query(Message).filter(Message.sender_name == name).first()
            return result
        except Exception as e:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return result
    else:
        return "Wrong JWT Token"

@app.get("/get_message_by_reciever")
async def get_message_by_sender(name: str, db: db_dependency):
    if (check_user_roles()):
        try:
            result = db.query(Message).filter(Message.receiver_name == name).first()
            return result
        except Exception as e:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return result
    else:
        return "Wrong JWT Token"


@app.delete("/delete_message")
async def delete_message(message_id: int, db: db_dependency):
    if (check_user_roles()):
        try:
            message = db.query(Message).filter(Message.id == message_id).first()
            db.delete(message)
            db.commit()
            return "Success"
        except Exception as e:
            return "Cant find message"
    else:
        return "Wrong JWT Token"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
