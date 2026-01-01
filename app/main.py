from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, status
from app.db import init_db, engine
from app.models import User
from app import models, auth
from sqlmodel import Session, select

app = FastAPI(title="Simple Admin API")
init_db()

@app.post("auth/register")
def register(username: str, email: str, password: str) -> dict:
    hashed = auth.get_password_hash(password=password)

    with Session(engine) as sess:
        user = User(username=username, email=email, hashed_password=hashed)
        sess.add(user)
        sess.commit()
        sess.refresh(user)

    response = {
        "id": user.id,
        "username": user.username
    }
    return response

@app.post("auth/login")
def login(username: str, password: str):
    with Session(engine) as sess:
        user = sess.exec(select(User).where(User.username == username)).first()

        if not user or not auth.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid Credentials")
        
        data = {
            "sub": user.username,
            "user_id": user.id
        }
        token = auth.create_access_token(data=data)

        response = {
            "access_token": token,
            "token_type": "bearer"
        }
        return response

@app.post("/packages/{packages_id}/upload")
def upload_file(packages_id: int):
    pass