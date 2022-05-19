from typing import Union
from os import getcwd
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

app = FastAPI()

@app.post("/file")
async def create_file(file: UploadFile = File(...)):
    with open( getcwd() + "/" + file.filename, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close() 
    return "success"

@app.get("/file/{name_file}")
async def get_file(name_file: str):
    return FileResponse(getcwd() + "/" + name_file)

@app.get("/predict/file/{name_file}")
async def get_file_predict(name_file: str, ds: Union[str, None] = "ds", y: Union[str, None] = "y", p: int = 365, f: Union[str, None] = "d"):
    
    try:
    
        df = pd.read_csv(f'{getcwd()}/{name_file}',date_parser=True)
        df = df.rename(columns={ds:'ds', y:'y'})
        delete = list(df.columns)
        delete.remove('ds')
        delete.remove('y')
        df = df.drop(delete, axis=1)
        df = df.dropna()

        df['ds'] = pd.to_datetime(df['ds'], infer_datetime_format=True)
        print(df.dtypes)
        m = Prophet()
        m.fit(df)

        future = m.make_future_dataframe(periods=p, freq=f)

        forecast = m.predict(future)

        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(f"Predict_{name_file[:-4]}.csv", index=False)

        return FileResponse(getcwd() + "/" + f"Predic_{name_file[:-4]}.csv")
    except Exception as err:
        print(err)
        return "unsuccess"

@app.get("/predict/graph/{name_file}")
async def get_graph_predict(name_file: str, ds: Union[str, None] = "ds", y: Union[str, None] = "y", p: int = 365, f: Union[str, None] = "d"):

    try:
        df = pd.read_csv(f'{getcwd()}/{name_file}',date_parser=True)
        df = df.rename(columns={ds:'ds', y:'y'})
        delete = list(df.columns)
        delete.remove('ds')
        delete.remove('y')
        df = df.drop(delete, axis=1)
        df = df.dropna()

        df['ds'] = pd.to_datetime(df['ds'], infer_datetime_format=True)
        print(df.dtypes)
        m = Prophet()
        m.fit(df)

        future = m.make_future_dataframe(periods=p, freq=f)

        forecast = m.predict(future)
        m.plot(forecast)

        plt.title("Predict using Prophet")
        plt.xlabel("ds")
        plt.ylabel("y")
        plt.savefig(f"Predict_{name_file[:-4]}.png")

        return FileResponse(getcwd() + "/" + f"Predict_{name_file[:-4]}.png")
    except Exception as err:
        print(err)
        return "unsuccess"