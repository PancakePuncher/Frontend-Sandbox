import strawberry
import random
from database.utility.db_util_init import db_connection, Items, all_item_ids
from strawberry.asgi import GraphQL


@strawberry.type
class Item:
    id: int
    name: str
    desc: str
    icon64: str


@strawberry.type
class Question:
    question: str


@strawberry.type
class Query:
    @strawberry.field
    async def randitem(self) -> Item:
        random_item = random.choice(all_item_ids)
        async with db_connection:
            item = await Items.select().where(Items.id == random_item).get()
        return Item(
            id=item.id,
            name=item.name,
            desc=item.description,
            icon64=item.base64_icon_large,
        )

    @strawberry.field
    async def randQuestion(self) -> Question:

        return Question(question="I am a random question.")


item_schema = GraphQL(strawberry.Schema(query=Query))
