import strawberry
import random
from database.utility.db_util_init import (
    master_db,
    Items,
    Questions,
    ItemsQuestionsCombo,
    global_item_id_lst,
    global_question_id_lst,
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

        if len(global_item_id_lst) > 1:
            random_item = random.choice(global_item_id_lst)
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

        if len(global_question_id_lst) > 1:
            random_question = random.choice(global_question_id_lst)
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


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def receiveUserAnswer(
        self, answer: int, questionId: int, itemId: int
    ) -> None:
        async with master_db.connection():
            question = (
                await Questions.select()
                .where(Questions.pk_question_id == questionId)
                .get()
            )
            question.question_answered_int += 1
            if answer == 1:
                truthy = 1
                falsy = 0
                question.question_truthy_int += 1
            if answer == 0:
                falsy = 1
                truthy = 0
                question.question_falsy_int += 1
            await question.save()

            look_for_record = (
                await ItemsQuestionsCombo.select()
                .where(ItemsQuestionsCombo.fk_item_id == itemId)
                .get()
            )

            if look_for_record is None:
                await ItemsQuestionsCombo.create(
                    fk_item_id=itemId,
                    fk_question_id=questionId,
                    question_truthy_int=truthy,
                    question_falsy_int=falsy,
                )
            elif look_for_record is not None:

                look_for_record.question_truthy_int += truthy
                look_for_record.question_falsy_int += falsy

                await look_for_record.update(
                    {
                        "question_truthy_int": look_for_record.question_truthy_int,
                        "question_falsy_int": look_for_record.question_falsy_int,
                    }
                ).where(ItemsQuestionsCombo.fk_item_id == itemId)

        return


graphql_schema = GraphQL(strawberry.Schema(query=Query, mutation=Mutation))
