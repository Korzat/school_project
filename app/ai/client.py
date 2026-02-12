import google.genai as genai
from app.core.config import settings


client = genai.Client(api_key=settings.API_KEY)
