## 🧠 Proposed Methodology

### 1. Data Cleaning & Normalization
- Deduplication and missing value handling  
- Standardization of merchant descriptions  
- Conversion of raw transactions into analytical time-series formats  

### 2. Spending Categorization
- Rule-based and NLP-assisted classification  
- Category aggregation at daily, weekly, and monthly levels  
- Detection of irregular or uncategorized transactions  

### 3. Time-Series Forecasting
- Monthly expense forecasting using **Facebook Prophet**  
- Trend, seasonality, and change-point detection  
- Forward-looking projections to anticipate future spending patterns  

### 4. NLP & Semantic Understanding
- **RoBERTa-based sentiment analysis** applied to transaction descriptions  
- Detection of emotionally charged or unusual spending behavior  
- Embedding generation for semantic similarity and clustering  

### 5. Multi-Agent AI Workflow (CrewAI)
A coordinated group of AI agents performs specialized tasks:
- Insight generation agent  
- Anomaly detection agent  
- Savings recommendation agent  
- Summary and explanation agent  

These agents collaborate using shared context and vector search (Qdrant) to produce coherent, personalized insights.
