import peewee
import asyncio
from peewee_aio import Manager

master_db = Manager("aiosqlite:///database/osrs.db")
db_connection = master_db.connection()


class Items(master_db.Model):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField()
    description = peewee.CharField()
    members = peewee.BooleanField()
    base64_icon = peewee.CharField()
    base64_icon_large = peewee.CharField()

async def get_all_item_ids():
    id_list =[]
    async with db_connection:
        async for item in Items.select():
            assert item.id
            id_list.append(item.id)

    return id_list


all_item_ids = asyncio.run(get_all_item_ids())