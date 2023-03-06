import pandas as pd
import platform
import sys
import uvicorn
import typing
import strawberry
from strawberry.asgi import GraphQL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
data = pd.read_feather("./data/items.feather")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


def get_rand_item():

    data = pd.read_feather("./data/items.feather")
    random_item = data.sample()
    item_dict = random_item.to_dict("records")

    return item_dict[0]


@strawberry.type
class Item:
    id: int
    name: str
    icon64: str
    iconUrl: str
    desc: str


@strawberry.type
class Query:
    @strawberry.field
    def item(self) -> Item:
        item = get_rand_item()
        return Item(
            id=item["id"],
            name=item["name"],
            icon64=item["base64_icon_large"],
            iconUrl=item["icon_large"],
            desc=item["description"],
        )


schema = strawberry.Schema(query=Query)
app.add_route("/item", GraphQL(schema))


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
