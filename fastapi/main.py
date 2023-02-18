import pandas as pd
import platform
import sys
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/new_item")
async def home():

    data = pd.read_feather("./data/data.feather")
    random_item = data.sample()

    return {"ItemData" : random_item.to_dict("records")}

if __name__ == "__main__":

    ip = "0.0.0.0"

    if platform.system() == "Windows":
        ip = "127.0.0.1"
    elif platform.system() == "Linux":
        ip = "0.0.0.0"
        
    sys.dont_write_bytecode = True
    uvicorn.run("main:app",
            host=ip,
            port=8000,
            reload=True,
            )