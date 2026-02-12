# from openai import OpenAI
#
# client = OpenAI(api_key=settings.API_KEY)
#
# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "user", "content": "Напиши односоставную сказку на ночь про единорога."}
#     ]
# )
#
# # Генерируемый текст находится в response.choices[0].message.content
# print(response.choices[0].message.content)
import os

from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI

client = OpenAI(api_key=os.getenv("API_KEY"))

