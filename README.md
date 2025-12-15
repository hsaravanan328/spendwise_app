# SpendWise App

SpendWise is a personal finance dashboard that helps you track, analyze, and manage your spending. It provides insights into your financial habits, helps you create budgets, and even offers a glimpse into your future spending patterns.

## 🚀 Features

The application is organized into several key modules:

-   **💸 Spending Insights**: Get a high-level overview of your spending habits and financial health.
-   **📊 Category Dashboard**: Visualize your spending breakdown across different categories.
-   **🗓️ Budget Planner**: Create and manage your personal budget to stay on track.
-   **📈 Spending Forecast**: Leverage predictive analytics to forecast your future expenses.
-   **😊 Sentiment Analysis**: Analyze the sentiment behind your spending descriptions.

---

## 🔍 Project Overview

Managing personal finances is often fragmented across spreadsheets, banking apps, and static reports, offering limited foresight or personalized guidance.  
SpendWise addresses this gap by providing:

- Automated transaction preprocessing and enrichment  
- Intelligent categorization of spending behavior  
- Forecasting of future expenses using time-series models  
- AI-generated insights, anomaly detection, and savings recommendations  
- A single, user-friendly analytics interface for financial decision-making  

The platform is designed to simulate a **personal financial analyst**, continuously interpreting user data and surfacing meaningful insights.

---

## 📊 Data Used

The system operates on structured financial transaction data, typically exported from banking or budgeting platforms.

**Core data fields include:**
- Transaction date  
- Description / merchant name  
- Transaction amount  
- Debit / credit indicator  
- Account or category metadata (when available)

**Derived features created during preprocessing:**
- Standardized merchant names  
- Normalized spending categories  
- Monthly and category-level aggregates  
- Sentiment-enriched transaction descriptions  
- Vector embeddings for semantic similarity search  

The architecture is flexible and supports additional enrichment sources as needed.

---

## 📈 Visualizations (To Be Added)

The Streamlit dashboard includes:
- Monthly spending trends  
- Category-wise expense breakdowns  
- Forecasted vs historical expense curves  
- Detected anomalies and outliers  
- AI-generated narrative insights  

> Visual examples and screenshots will be added in a future update.

---

## 🧾 Concise Interpretation of Results

SpendWise converts raw transaction logs into:
- Clear visibility of where money is being spent  
- Early warnings for unusual or risky spending behavior  
- Forward-looking forecasts that reduce financial uncertainty  
- Context-aware explanations rather than static charts  

By combining quantitative forecasts with qualitative AI insights, users gain both **numerical clarity and narrative understanding** of their finances.

---

## 💼 Business Outcome for Stakeholders

### For End Users
- Improved budgeting discipline  
- Better anticipation of future expenses  
- Personalized recommendations rather than generic advice  

### For Financial Platforms / FinTech Teams
- Demonstrates how AI agents can enhance financial analytics  
- Scalable architecture adaptable to consumer or SMB finance tools  
- Reduced manual analysis through automation  

SpendWise is not just a data project — it is a **decision-support system**.

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Data Processing:** Pandas  
- **Forecasting:** Prophet  
- **NLP:** RoBERTa  
- **Vector Database:** Qdrant  
- **AI Orchestration:** CrewAI  
- **Frontend:** Streamlit  
- **Version Control:** Git & GitHub  

---


## ▶️ Hosted Site

Visit https://spendwiseapp.streamlit.app/ in your web browser to start using SpendWise App.
