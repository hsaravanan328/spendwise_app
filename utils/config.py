import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("❌ Missing GOOGLE_API_KEY in .env")

genai.configure(api_key=API_KEY)

# ✔ valid model from your list
MODEL_NAME = "models/gemini-2.5-flash"
