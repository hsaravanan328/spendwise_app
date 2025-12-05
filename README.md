# SpendWise App

SpendWise is a personal finance dashboard that helps you track, analyze, and manage your spending. It provides insights into your financial habits, helps you create budgets, and even offers a glimpse into your future spending patterns.

## 🚀 Features

The application is organized into several key modules:

-   **💸 Spending Insights**: Get a high-level overview of your spending habits and financial health.
-   **📊 Category Dashboard**: Visualize your spending breakdown across different categories.
-   **🗓️ Budget Planner**: Create and manage your personal budget to stay on track.
-   **📈 Spending Forecast**: Leverage predictive analytics to forecast your future expenses.
-   **😊 Sentiment Analysis**: Analyze the sentiment behind your spending descriptions.

## Project Structure

The project is organized into the following directories:

-   **/app.py**: The main entry point for the Streamlit application.
-   **/pages/**: Contains the individual Streamlit pages for each feature.
-   **/agents/**: Holds the core business logic for analysis, categorization, and financial coaching.
-   **/utils/**: Includes utility functions for data loading, cleaning, configuration, and styling.
-   **/data/**: The default directory for storing transaction data.
`note: make sure your data has the following columns: ["Details", "Posting Date", "Description", "Amount", "Balance"]`
-   **styles.css**: Custom CSS for visual styling of the application.
-   **requirements.txt**: A list of all Python dependencies required to run the project.

## ⚙️ Setup and Installation

Follow these steps to get the application running on your local machine.

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # For Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install Dependencies**
    Make sure you have all the required packages by running:
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Running the Application

Once the setup is complete, you can launch the Streamlit application with the following command:

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your web browser to start using SpendWise Agent.

## ▶️ Hosted Site

Visit https://spendwiseapp.streamlit.app/ in your web browser to start using SpendWise App.
