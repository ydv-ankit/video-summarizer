from fastapi import FastAPI, UploadFile
import math
import random
import os
import video_processing

# FastAPI instance
app = FastAPI()

@app.get("/")
def root():
    return {"msg":"success"}

@app.post("/upload")
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