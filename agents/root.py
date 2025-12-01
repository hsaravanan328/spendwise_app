from agents.analyzer import analyze_spending
from agents.coach import coach_user

def run_root_agent(prompt, df):
    analysis = analyze_spending(prompt, df)
    advice = coach_user(analysis, prompt)
    return analysis, advice
