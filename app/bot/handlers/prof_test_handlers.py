from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.prof_test_keyboards import result_keyboard, yes_no_keyboard
from app.bot.keyboards.start_keyboard import reply_keyboard_start
from app.db.crud.users_crud import question_yes, reset_points, get_user_points
from aiogram.fsm.context import FSMContext
from app.bot.handlers.states import TestPass

prof_test_router = Router()

questions = [
"Вам нравится решать логические задачи, головоломки или играть в шахматы?",
"Вы предпочитаете работать с числами, формулами и расчетами, а не с текстами или людьми?",
"Вы любите разбираться, как работают механизмы, устройства или компьютерные программы?",
"Вам нравится находить ошибки, неточности и несостыковки в документах или коде?",
"Вы чувствуете себя комфортно, работая в условиях четких инструкций, правил и алгоритмов?",
"В школе или университете вам легче давались точные науки (математика, физика, информатика), чем гуманитарные (литература, история)?",
"Вам нравится структурировать информацию, организовывать данные в таблицы или схемы?",
"Вы усидчивы и можете долго концентрироваться на одной задаче, требующей внимания к деталям?",
"Вас привлекает идея создавать что-то новое (программу, мост, систему), а не просто обслуживать текущие процессы?",
"Вы считаете, что в большинстве ситуаций существует единственное правильное, логическое решение?"
]


@prof_test_router.message(F.text == "Пройти профориентационный тест")
async def start_prof_test_handler(message: Message, session: AsyncSession, state: FSMContext):
    await reset_points(message.from_user.id, session)

    await state.set_state(TestPass.answering_question)
    await state.update_data(current_question_index=0)

    await message.answer(
        questions[0],
        reply_markup=await yes_no_keyboard()
    )

@prof_test_router.message(TestPass.answering_question, F.text.in_({"Да", "Нет"}))
async def process_answer_handler(message: Message, session: AsyncSession, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id

    user_data = await state.get_data()
    current_index = user_data.get("current_question_index", 0)

    if user_answer == "Да":
        await question_yes(user_id, session)

    next_index = current_index + 1

    if next_index < len(questions):
        await state.update_data(current_question_index=next_index)
        await message.answer(questions[next_index], reply_markup=await yes_no_keyboard())
    else:
        await state.clear()
        await message.answer(
            "Тест окончен, нажмите кнопку, чтобы узнать результат",
            reply_markup=await result_keyboard()
        )

@prof_test_router.message(TestPass.answering_question)
async def invalid_answer_handler(message: Message):
    await message.answer("Пожалуйста, ответьте 'Да' или 'Нет', используя кнопки ниже.")

@prof_test_router.callback_query(F.data == "show_result")
async def show_result_callback_handler(callback: CallbackQuery, session: AsyncSession):
    try:
        points = await get_user_points(callback.from_user.id, session)
        if points <=3:
            await callback.message.answer(f"""Вам, скорее всего, подойдут профессии, требующие большего взаимодействия с людьми, коммуникации, анализа сложных социальных или правовых ситуаций.
🔑 Ваши потенциальные профессии: <b><u>Юрист</u></b>, <b><u>Медик</u></b> (в зависимости от эмпатии и интереса к биологии).

Обратите внимание: этот мини-тест является упрощенным и создан для развлечения. Он не может заменить полноценную консультацию с профориентологом.""",parse_mode="HTML", reply_markup=await reply_keyboard_start())
        elif points <=7:
            await callback.message.answer(f"""Вы обладаете универсальным складом ума и можете быть успешны как в точных науках, так и в аналитической работе. Вам подойдет работа, требующая системного подхода.
🔑 Ваши потенциальные профессии: <b><u>Экономист</u></b>, <b><u>Инженер</u></b>.

Обратите внимание: этот мини-тест является упрощенным и создан для развлечения. Он не может заменить полноценную консультацию с профориентологом.""",parse_mode="HTML", reply_markup=await reply_keyboard_start())
        elif points <=10:
            await callback.message.answer(f"""У вас ярко выраженный технический и логический склад ума. Вы любите системы, алгоритмы, детали и точные науки.
🔑 Ваши потенциальные профессии: <b><u>Программист</u></b>, <b><u>Инженер</u></b>.

Обратите внимание: этот мини-тест является упрощенным и создан для развлечения. Он не может заменить полноценную консультацию с профориентологом.""",parse_mode="HTML", reply_markup=await reply_keyboard_start())
        else:
            await callback.message.answer(f"Ошибка при получении результатов", reply_markup=await reply_keyboard_start())
        await callback.answer()
    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")
        await callback.answer()
