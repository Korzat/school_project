from app.ai.client import client
from app.ai.prompts import PROFESSION_PROMPTS

model_name = "gemini-2.5-flash"

async def response_by_profession_subjects(profession_name: str):
    try:
        if profession_name in PROFESSION_PROMPTS:
            return PROFESSION_PROMPTS[profession_name]["subjects"]

        prompt = f'''Выдать список школьных предметов, нужных для сдачи ЕГЭ в 2025/2026 г. для поступления на профессию "{profession_name}" в г. Москва. Оформить в деловом стиле.'''

        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text

    except Exception as e:
        print("Gemini error:", e)
        return "Извините, сервис временно недоступен. Попробуйте позже."




async def response_by_info_about_profession(profession_name: str):
    try:
        if profession_name in PROFESSION_PROMPTS:
            return PROFESSION_PROMPTS[profession_name]["info"]

        prompt = f'''Выдать информацию по профессии: "{profession_name}" в г. Москва. Оформить в деловом стиле.'''

        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text

    except Exception as e:
        print("Gemini error:", e)
        return "Извините, сервис временно недоступен. Попробуйте позже."

async def ask_ai_question(question: str):
    try:
        prompt = f"{question}\n\nОтветь кратко и по существу, максимум 500 слов."
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        answer = response.text
        if len(answer) > 3500:
            answer = answer[:3500] + "..."
        return answer
    except Exception as e:
        print("Gemini error:", e)
        return "Извините, сервис временно недоступен. Попробуйте позже."