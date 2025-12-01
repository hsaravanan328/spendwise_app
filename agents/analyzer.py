import google.generativeai as genai
from utils.config import MODEL_NAME

def analyze_spending(question, df):
    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
You are SpendWise, a friendly financial helper.

User question:
{question}

Here are their transactions:
{df.to_dict(orient="records")}

Provide:
- A simple explanation of what's going on in their spending
- Mention any patterns, spikes, or interesting observations
- Keep it short and friendly (2–3 sentences)
- No lists, no bullet points — just a natural explanation
"""

    resp = model.generate_content(prompt)
    return resp.text.strip()
