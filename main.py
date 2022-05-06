from os import getcwd
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File

app = FastAPI()
@app.get("/")
async def prueba():
    return "Hola :D"

@app.post("/file/")
async def create_upload_file(file: UploadFile = File(...)):
    with open( getcwd() + "/" + file.filename, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close() 
    return "success"

@app.get("/file/{name_file}")
async def get_file(name_file: str):
    return FileResponse(getcwd() + "/" + name_file)