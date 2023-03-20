import strawberry
import random
from database.utility.db_util_init import (
    master_db,
    Items,
    Questions,
    all_item_ids,
    all_question_ids,
)
from strawberry.asgi import GraphQL


@strawberry.type
class Item:
    itemId: int = None
    itemName: str = None
    itemDesc: str = None
    itemIcon64: str = None


@strawberry.type
class Question:
    questionId: int = None
    questionText: str = None
    questionOff: int = None
    questionT: int = None
    questionF: int = None


@strawberry.type
class Query:
    @strawberry.field
    async def randItem(self) -> Item:

        if len(all_item_ids) > 1:
            all_item_ids.pop(0)
            random_item = random.choice(all_item_ids)
        else:
            random_item = 0
        async with master_db.connection():
            item = await Items.select().where(Items.pk_item_id == random_item).get()
        return Item(
            itemId=item.pk_item_id,
            itemName=item.item_name_str,
            itemDesc=item.item_description_str,
            itemIcon64=item.base64_icon_large_str,
        )

    @strawberry.field
    async def randQuestion(self) -> Question:

        if len(all_question_ids) > 1:
            all_question_ids.pop(0)
            random_question = random.choice(all_question_ids)
        else:
            random_question = 0
        async with master_db.connection():
            question = (
                await Questions.select()
                .where(Questions.pk_question_id == random_question)
                .get()
            )
            question.question_offered_int = question.question_offered_int + 1
            await question.save()

        return Question(
            questionId=question.pk_question_id,
            questionText=question.question_text_str,
            questionOff=question.question_offered_int,
            questionT=question.question_truthy_int,
            questionF=question.question_falsy_int,
        )


item_schema = GraphQL(strawberry.Schema(query=Query))
