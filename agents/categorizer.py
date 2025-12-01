import google.generativeai as genai
from utils.config import MODEL_NAME

def categorize_transaction(description, details=None):
    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
You are a bank transaction categorizer.

Choose ONE category:
Groceries, Dining, Coffee, Shopping, Transport, Travel, Health, Entertainment,
Bills, Utilities, Education, Subscriptions, Income, Other.

Description: {description}
Details: {details}

Return only the category name.
"""

    resp = model.generate_content(prompt)
    return resp.text.strip()
