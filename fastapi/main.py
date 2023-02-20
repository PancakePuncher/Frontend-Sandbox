import pandas as pd
import platform
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://pancakepuncher-literate-winner-vgj6q66w9wh69w9-3000.preview.app.github.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/new_item")
async def home():

    data = pd.read_feather("./data/items.feather")
    random_item = data.sample()

    return {"ItemData" : random_item.to_dict("records")}

if __name__ == "__main__":

    ip = "0.0.0.0"

    if platform.system() == "Windows":
        ip = "127.0.0.1"
    elif platform.system() == "Linux":
        ip = "0.0.0.0"
    
    print("Starting...")
    sys.dont_write_bytecode = True
    uvicorn.run("main:app",
            host=ip,
            port=8000,
            reload=True,
            )