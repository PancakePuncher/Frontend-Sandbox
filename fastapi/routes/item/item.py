import strawberry
import random
from database.utility.db_util_init import db_connection, Items, all_item_ids
from strawberry.asgi import GraphQL


@strawberry.type
class Item:
    id: int = None
    name: str = None
    desc: str = None
    icon64: str = None


@strawberry.type
class Question:
    question: str = None


@strawberry.type
class Query:
    @strawberry.field
    async def randitem(self) -> Item:
        if len(all_item_ids) > 0:
            all_item_ids.pop(0)
            random_item = random.choice(all_item_ids)
        else:
            random_item = 0
        async with db_connection:
            item = await Items.select().where(Items.pk_id == random_item).get()
        return Item(
            id=item.pk_id,
            name=item.item_name_str,
            desc=item.item_description_str,
            icon64=item.base64_icon_large_str,
        )

    @strawberry.field
    async def randQuestion(self) -> Question:

        return Question(question="I am a random question.")


item_schema = GraphQL(strawberry.Schema(query=Query))
