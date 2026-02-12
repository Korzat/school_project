import google.generativeai as genai
from app.core.config import settings


genai.configure(api_key=settings.API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

