import google.generativeai as genai
from utils.config import MODEL_NAME

def coach_user(analysis, question):
    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
You are SpendWise, a warm, friendly financial coach. 
You speak like a supportive friend who understands student life, budgeting stress, and real spending habits.

User question:
{question}

Spending analysis:
{analysis}

Give advice that is:
- Simple and easy to follow
- Supportive, not judgmental
- Friendly and human (like talking to a friend)
- Short: 2 to 4 sentences max
- Includes at least one practical next step

Write in a conversational tone. Avoid generic tips.
"""

    resp = model.generate_content(prompt)
    return resp.text.strip()
