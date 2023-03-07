import strawberry
import peewee
import aiosqlite
import asyncio
import random
from peewee_aio import Manager
from strawberry.asgi import GraphQL

manager = Manager("aiosqlite:///database/osrs.db")
connection = manager.connection()


async def get_all_item_ids():

    db = await aiosqlite.connect("database/osrs.db")
    cursor = await db.execute("SELECT ID FROM items")
    rows = await cursor.fetchall()
    await cursor.close()
    await db.close()

    id_list = []
    for i in rows:
        id_list.append(i[0])

    return id_list


all_item_ids = asyncio.run(get_all_item_ids())


class Items(manager.Model):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField()
    description = peewee.CharField()
    members = peewee.BooleanField()
    base64_icon = peewee.CharField()
    base64_icon_large = peewee.CharField()


@strawberry.type
class Item:
    id: int
    name: str
    desc: str
    icon64: str


@strawberry.type
class Query:
    @strawberry.field
    async def item(self) -> Item:
        random_item = random.choice(all_item_ids)
        async with connection:
            item = await Items.select().where(Items.id == random_item).get()
        return Item(
            id=item.id,
            name=item.name,
            desc=item.description,
            icon64=item.base64_icon_large,
        )


item_schema = GraphQL(strawberry.Schema(query=Query))
