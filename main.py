from fastapi import FastAPI, UploadFile, File

app = FastAPI()
@app.get("/")
async def prueba():
    return "Hola :D"

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}