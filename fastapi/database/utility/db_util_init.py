import peewee
import asyncio
from pathlib import Path
from peewee_aio import Manager

database_file = Path("./database/osrs.db")

master_db = Manager("aiosqlite:///database/osrs.db")
db_connection = master_db.connection()


class Items(master_db.Model):
    pk_item_id = peewee.IntegerField(primary_key=True)
    item_name_str = peewee.CharField()
    item_description_str = peewee.CharField()
    item_members_bool = peewee.BooleanField()
    base64_icon_str = peewee.CharField()
    base64_icon_large_str = peewee.CharField()

class Questions(master_db.Model):
    pk_question_id = peewee.IntegerField(primary_key=True)
    question_text_str = peewee.CharField()
    question_offered_int = peewee.IntegerField()
    question_answered_int = peewee.IntegerField()
    question_truthy_int = peewee.IntegerField()
    question_falsy_int = peewee.IntegerField()

async def create_database():

    if database_file.is_file() is False:
        open("./database/osrs.db", "w")
        await Items.create_table()

    async with db_connection:
        test_query = await Items.select().where(Items.pk_item_id == 0)
        if len(test_query) == 0:
            await Items.create(
                pk_item_id=0,
                item_name_str="Default Item",
                item_description_str="Check your /database/osrs.db file...",
                item_members_bool="True",
                base64_icon_str="Default",
                base64_icon_large_str="Default",
            )
    await Questions.create_table()
    async with db_connection:
        test_query = await Questions.select().where(Questions.pk_question_id == 0)
        if len(test_query) == 0:
            await Questions.create(
                pk_question_id = 0,
                question_text_str = "Default Question",
                question_offered_int = 0,
                question_answered_int = 0,
                question_truthy_int = 0,
                question_falsy_int = 0,
            )
    return True


async def prep_id_arrs(database_status):

    item_id_list = []

    if database_status is True:
        async with db_connection:
            async for i in Items.select():
                assert i
                item_id_list.append(i)
    
    question_id_list = []

    if database_status is True:
        async with db_connection:
            async for q in Questions.select():
                assert q
                question_id_list.append(q)

    return item_id_list, question_id_list


database_status = asyncio.run(create_database())

all_item_ids, all_question_ids = asyncio.run(prep_id_arrs(database_status))
