import peewee
import asyncio
from pathlib import Path
from peewee_aio import Manager

database_file = Path("./database/osrs.db")

master_db = Manager("aiosqlite:///database/osrs.db")
db_connection = master_db.connection()


class Items(master_db.Model):
    pk_item_id = peewee.IntegerField(primary_key=True)
    item_name_str = peewee.CharField(default="Default Item")
    item_description_str = peewee.CharField(
        default="Check your /database/osrs.db file..."
    )
    item_members_bool = peewee.BooleanField(default=True)
    base64_icon_str = peewee.CharField(default="Default")
    base64_icon_large_str = peewee.CharField(default="Default")


class Questions(master_db.Model):
    pk_question_id = peewee.AutoField(primary_key=True)
    question_text_str = peewee.CharField(default="Default Question", unique=True)
    question_offered_int = peewee.IntegerField(default=0)
    question_answered_int = peewee.IntegerField(default=0)
    question_truthy_int = peewee.IntegerField(default=0)
    question_falsy_int = peewee.IntegerField(default=0)


class ItemsQuestionsCombo(master_db.Model):
    pk_combo_index = peewee.AutoField(primary_key=True)
    fk_item_id = peewee.ForeignKeyField(Items, to_field="pk_item_id", unique=True)
    fk_question_id = peewee.ForeignKeyField(
        Questions, to_field="pk_question_id", unique=False
    )
    question_truthy_int = peewee.IntegerField(default=0)
    question_falsy_int = peewee.IntegerField(default=0)


async def create_database():

    default_questions = [
        {"question_text_str": "Can you equip this item?"},
        {"question_text_str": "Can you eat this item?"},
        {"question_text_str": "Can you drop this item?"},
        {"question_text_str": "Can you trade this item?"},
        {"question_text_str": "Do you need a stat requirement to use this item?"},
        {"question_text_str": "Do you need this item for a quest?"},
        {"question_text_str": "Can you only get this item after doing a quest?"},
        {"question_text_str": "Can you gather this item using a skill?"},
        {"question_text_str": "Can you only get this item from a monster drop?"},
        {"question_text_str": "Can you craft this item?"},
    ]

    item_id_list = []
    question_id_list = []

    if database_file.is_file() is False:
        open("./database/osrs.db", "w")

    await Items.create_table()
    await Questions.create_table()
    await ItemsQuestionsCombo.create_table()

    async with db_connection:
        test_query = await Items.select()
        if len(test_query) == 0:
            await Items.create()
        elif len(test_query) > 0:
            async for i in Items.select():
                assert i
                item_id_list.append(i.pk_item_id)

    async with db_connection:
        test_query = await Questions.select()
        if len(test_query) == 0:
            for data_dict in default_questions:
                await Questions.create_or_get(**data_dict)
        elif len(test_query) > 0:
            async for q in Questions.select():
                assert q
                question_id_list.append(q.pk_question_id)

    return item_id_list, question_id_list


global_item_id_lst, global_question_id_lst = asyncio.run(create_database())
