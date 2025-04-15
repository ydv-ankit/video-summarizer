from fastapi import FastAPI, UploadFile
import math
import random
import os
import schemas.user
import video_processing
from fastapi import Depends, HTTPException
from db.engine import db_connection, engine
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
import models.user as user_model
from pydantic import BaseModel
import schemas
import uuid
import bcrypt

user_model.Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI()

@app.get("/health")
def root():
    return {"msg":"success"}

@app.post("/upload", status_code=200)
async def create_upload_file(file: UploadFile):
    # create a random filename
    filename: str = str(math.floor(random.random() * 10e10)) + "." + file.filename.split(".")[-1]
    # check and create "tmp" directory
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    # read the file contents and write to a new file inside "tmp" directory
    contents = await file.read()
    with open(f"tmp/{filename}", "wb") as f:
        f.write(contents)
    
    # extract audio from video
    summary_data = video_processing.process_video(f"tmp/{filename}")
    return {"msg": "video processed", "data": summary_data or None}

@app.post("/signup", status_code=201)
def signup(
    user: schemas.user.UserBase,
    db: Session = Depends(db_connection)
):
    try:
        # unique uuid -> user id
        id = uuid.uuid4()
        # generate hashed password
        hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt(12))
        query = insert(user_model.User).values(id=id, email = user.email, password = hashed_password.decode())
        db.execute(query)
        db.commit()
        return {"msg": "success", "data": id}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="user already exists")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login", status_code=200)
def login(
        user: schemas.user.UserBase,
        db: Session = Depends(db_connection)
    ):
    try:
        # check if user exists
        query = select(user_model.User).where(user_model.User.email == user.email)
        res = db.scalars(query).first()
        # if exists, check password
        if res:
            if bcrypt.checkpw(bytes(user.password, 'utf-8'), bytes(res.password, 'utf-8')):
                return {
                    "msg": "success",
                    "data": res.id
                }
            else:
                raise HTTPException(status_code=401, detail="invalid password")
        else:
            # raise unauthorised error
            raise HTTPException(status_code=401, detail="login failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))