from fastapi import FastAPI, UploadFile, Depends, HTTPException
import math
import random
import os
import schemas.user
import video_processing
from fastapi.responses import JSONResponse
from db.engine import db_connection, engine
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
import models.user as user_model
from pydantic import BaseModel
import schemas
import uuid
import bcrypt
import jwt
import env

user_model.Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI()

@app.get("/health")
def root():
    return JSONResponse({"msg":"success"}, 200)

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
    return JSONResponse({"msg": "video processed", "data": summary_data or None}, 200)

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
        return JSONResponse({"id": id.__str__()}, 201)
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
                # generate jwt token
                token = jwt.encode({"id": res.id.__str__()}, env.JWT_SECRET, algorithm="HS256")
                # makeup json response structure
                response = JSONResponse({"id": res.id.__str__()}, 200)
                response.set_cookie(key="token", value=token)
                return response
            else:
                raise HTTPException(status_code=401, detail="invalid password")
        else:
            # raise unauthorised error
            raise HTTPException(status_code=401, detail="login failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tokens")
def get_tokens(userid: str):
    pass