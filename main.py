from fastapi import FastAPI, UploadFile, File

app = FastAPI()
@app.get("/")
async def prueba():
    return "Hola :D"

@app.post("/")
async def cargar_archivo(file: UploadFile = File(...)):
    print(file)
    return "Archivo cargado"