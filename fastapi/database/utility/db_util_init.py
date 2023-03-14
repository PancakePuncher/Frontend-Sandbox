import peewee
import asyncio
from pathlib import Path
from peewee_aio import Manager

database_file = Path("./database/osrs.db")

master_db = Manager("aiosqlite:///database/osrs.db")
db_connection = master_db.connection()


class Items(master_db.Model):
    pk_id = peewee.IntegerField(primary_key=True)
    item_name_str = peewee.CharField()
    item_description_str = peewee.CharField()
    item_members_bool = peewee.BooleanField()
    base64_icon_str = peewee.CharField()
    base64_icon_large_str = peewee.CharField()


async def create_database():

    open("./database/osrs.db", "w")
    await Items.create_table()
    async with db_connection:
        test_query = await Items.select().where(Items.pk_id == 0)
        if len(test_query) == 0:
            await Items.create(
                pk_id=0,
                item_name_str="I am a default Item...",
                item_description_str="If you're seeing this then your database didn't exist and Python created it.",
                item_members_bool="True",
                base64_icon_str="Default",
                base64_icon_large_str="Default",
            )
    return True


async def get_all_item_ids(database_status):

    id_list = []

    if database_status is True:
        async with db_connection:
            async for item in Items.select():
                assert item
                id_list.append(item)

    return id_list


if database_file.is_file() is False:
    database_status = asyncio.run(create_database())
else:
    database_status = True

all_item_ids = asyncio.run(get_all_item_ids(database_status))
