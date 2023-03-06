import pandas as pd
import platform
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.item.item import item_schema

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_route("/item", item_schema)


if __name__ == "__main__":

    ip = "0.0.0.0"

    if platform.system() == "Windows":
        ip = "127.0.0.1"
    elif platform.system() == "Linux":
        ip = "0.0.0.0"

    print("Starting...")
    sys.dont_write_bytecode = True
    uvicorn.run(
        "main:app",
        host=ip,
        port=8000,
        reload=True,
    )
