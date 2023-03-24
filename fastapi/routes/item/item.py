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
class PageDetails:
    itemId: int = None
    itemName: str = None
    itemDesc: str = None
    itemIcon64: str = None
    questionId: int = None
    questionText: str = None
    truthyValue: int or None = None
    falsyValue: int or None = None


@strawberry.type
class Query:
    @strawberry.field
    async def PageDetails(self) -> PageDetails:
        async with master_db.connection():
            if len(global_item_id_lst) > 1:
                random_item = random.choice(global_item_id_lst)
            else:
                random_item = 0

            item = await Items.select().where(Items.pk_item_id == random_item).get()

            if len(global_question_id_lst) > 1:
                random_question = random.choice(global_question_id_lst)
            else:
                random_question = 0
            question = (
                await Questions.select()
                .where(Questions.pk_question_id == random_question)
                .get()
            )

            question.question_offered_int = question.question_offered_int + 1
            await question.save()

            item_question_combo_record = (
                await ItemsQuestionsCombo.select()
                .where(
                    (ItemsQuestionsCombo.fk_item_id == random_item),
                    (ItemsQuestionsCombo.fk_question_id == random_question),
                )
                .get()
            )

            currentTruthyVal = 0
            currentFalsyVal = 0
            if item_question_combo_record is not None:
                currentTruthyVal = item_question_combo_record.question_truthy_int
                currentFalsyVal = item_question_combo_record.question_falsy_int

        return PageDetails(
            itemId=item.pk_item_id,
            itemName=item.item_name_str,
            itemDesc=item.item_description_str,
            itemIcon64=item.base64_icon_large_str,
            questionId=question.pk_question_id,
            questionText=question.question_text_str,
            truthyValue=currentTruthyVal,
            falsyValue=currentFalsyVal,
        )

    # @strawberry.field
    # async def itemGraphData(self) -> ItemData:
    #     async with master_db.connection():
    #         item_question_combo_record = await ItemsQuestionsCombo.select().where(
    #             (ItemsQuestionsCombo.fk_item_id == random_item)
    #             and (ItemsQuestionsCombo.fk_question_id == random_question)
    #         )

    #     return ItemData()


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
