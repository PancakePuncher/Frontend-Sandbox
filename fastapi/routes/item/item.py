import pandas as pd
import strawberry
from strawberry.asgi import GraphQL

data = pd.read_feather("./data/items.feather")

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

item_schema = GraphQL(strawberry.Schema(query=Query))