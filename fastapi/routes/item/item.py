import strawberry
import random
from database.utility.db_util_init import db_connection, Items, all_item_ids
from strawberry.asgi import GraphQL


@strawberry.type
class Item:
    item_id: int = None
    item_name: str = None
    item_desc: str = None
    item_icon64: str = None


@strawberry.type
class Question:
    question: str = None


@strawberry.type
class Query:
    @strawberry.field
    async def randItem(self) -> Item:
        if len(all_item_ids) > 0:
            all_item_ids.pop(0)
            random_item = random.choice(all_item_ids)
        else:
            random_item = 0
        async with db_connection:
            item = await Items.select().where(Items.pk_item_id == random_item).get()
        return Item(
            item_id=item.pk_item_id,
            item_name=item.item_name_str,
            item_desc=item.item_description_str,
            item_icon64=item.base64_icon_large_str,
        )

    @strawberry.field
    async def randQuestion(self) -> Question:

        return Question(question="I am a random question.")


item_schema = GraphQL(strawberry.Schema(query=Query))
