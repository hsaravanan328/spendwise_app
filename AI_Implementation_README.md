# 💰 SpendWise
*Your Personal AI-Powered Spending Assistant*

---

## ✅ **1. Overview / Description**

SpendWise is a Streamlit web application designed to help you take control of your personal finances. It transforms raw transaction data into clear, actionable insights. Instead of manually sifting through statements, you can use SpendWise to automatically analyze spending patterns, forecast future expenses, and even chat with an AI assistant about your financial habits.

This project is for anyone who wants a modern, intelligent, and visual way to understand their spending without the complexity of traditional finance software.

**Key Features:**
*   **📊 Interactive Dashboards**: Visualize spending by category, weekday, and transaction size.
*   **🤖 AI-Powered Forecasting**: Use a time-series model (`prophet`) to predict future spending based on historical data.
*   **💬 Conversational AI**: Ask questions about your finances in plain English and get instant answers from the "Ask SpendWise" agent.
*   **📈 Spending Insights**: Automatically generate charts for daily spending trends and weekly patterns.
*   **😊 Sentiment Analysis**: Analyze the sentiment of your transaction descriptions.
*   **📋 Budget Planning**: A dedicated module for planning and tracking your budget.

---

## ✅ **2. Tech Stack**

*   **Language**: Python
*   **Framework**: Streamlit
*   **Core Libraries**:
    *   `pandas`: For all data manipulation and analysis.
    *   `plotly`: For creating interactive, modern-looking charts.
    *   `prophet`: For the time-series forecasting feature.
    *   `google-generativeai`: Powers the "Ask SpendWise" conversational agent.
    *   `textblob` / `transformers`: Used for natural language processing tasks, including sentiment analysis.

---

## ✅ **3. Project Architecture**

SpendWise is a multi-page Streamlit application with a modular architecture.

1.  **Data Ingestion**: Transaction data is loaded via a utility function in `utils/loader.py`.
2.  **Frontend**: The entire UI is built with Streamlit. `app.py` serves as the main entry point and homepage.
3.  **Pages**: Each core feature is a separate Python script located in the `pages/` directory, which Streamlit automatically renders as a navigable page in the sidebar.
4.  **AI Agents**: The complex AI logic is encapsulated in the `agents/` directory. These agents handle tasks like categorization, analysis, and conversational responses.
5.  **Utilities**: Helper functions for data cleaning and other common tasks are stored in the `utils/` directory.

---

## ✅ **4. Folder Structure**

```
/
├── app.py                  # Main Streamlit application entry point
├── requirements.txt        # Python dependencies
├── styles.css              # Basic CSS for custom styling
├── pages/                  # Each .py file is a page in the app
│   ├── Spending_Insights.py
│   └── Spending_Forecast.py
├── agents/                 # Contains the logic for AI agents
│   ├── categorizer.py
│   └── root.py
├── utils/                  # Utility scripts for data loading, cleaning, etc.
│   ├── loader.py
│   └── data_cleaning.py
├── data/                   # Default location for storing transaction data
└── streamlit/              # Streamlit configuration
    └── secrets.toml        # For storing secrets like API keys
```

---

## ✅ **5. Installation Instructions**

**Prerequisites**:
*   Python 3.8+
*   An active internet connection to download dependencies.

**Steps**:
1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd spendwise_agent
    ```

2.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## ✅ **6. How to Run the Project**

Once the installation is complete, you can run the application with a single command:

```bash
streamlit run app.py
```

Your web browser should open a new tab with the SpendWise application running.

---

## ✅ **7. Configuration / Environment Variables**

This project uses Google's Generative AI, which requires an API key. This key should be stored securely.

1.  Create a file at `.streamlit/secrets.toml`.
2.  Add your Google API key to this file as follows:

    ```toml
    # .streamlit/secrets.toml

    GOOGLE_API_KEY = "your-api-key-here"
    ```

The application will automatically load this key for the "Ask SpendWise" agent.

---

## ✅ **8. Models / Agents**

*   **Forecast Agent** (`pages/Spending_Forecast.py`): This module uses Facebook's `prophet` library, a powerful time-series model. It analyzes historical debit transactions to generate a daily spending forecast for a user-selectable future period (e.g., 90 days).

*   **Conversational Agent** (`pages/Ask_Spendwise.py`): This agent is powered by `google-generativeai`. It allows you to have a natural language conversation about your financial data, providing quick summaries and answers.

*   **Categorizer Agent** (`agents/categorizer.py`): This agent contains the logic for automatically assigning categories to your transactions based on their descriptions.

---

## ✅ **9. Testing**

Currently, automated tests have not been implemented for this project. For future development, `pytest` would be the recommended testing framework.

To set it up, you would:
1.  Install pytest: `pip install pytest`
2.  Create a `tests/` directory.
3.  Write test functions (e.g., `test_data_loading()`).
4.  Run tests from the root directory with the `pytest` command.

---

## ✅ **10. Acknowledgements**

This project was made possible by the following incredible open-source libraries:
*   [Streamlit](https://streamlit.io/)
*   [Pandas](https://pandas.pydata.org/)
*   [Plotly](https://plotly.com/)
*   [Prophet](https://facebook.github.io/prophet/)
*   [Google Generative AI](https://ai.google.dev/)
