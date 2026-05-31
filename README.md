# AI-Powered Virtual Financial Advisor

An intelligent financial assistant designed to help bank customers analyze their spending, monitor financial health, detect anomalies, and receive autonomous, personalized generative AI advice.

---

## 🚀 Application Summary

This application acts as a virtual financial consultant by leveraging data analysis and Generative AI to deliver actionable financial insights.

* **Financial Trend Detection:** Process and aggregate historical data using `pandas` and `NumPy`.
* **Expense Classification:** Categorize transactions systematically using rule-based logic.
* **Natural Language Summaries:** Generate personalized, context-aware financial advice using `OpenAI` and `LangChain`.
* **Autonomous Reasoning:** Employs an agentic workflow to analyze financial behavior, detect risky patterns (e.g., high debt-to-income ratio), and identify missed opportunities (e.g., idle savings).
* **Interactive UI:** A clean, user-friendly dashboard built and deployed with `Streamlit`.

---

## 📂 Project Structure

```text
├── data/
│   └── customer_data.csv          # Sample dataset containing customer transaction history
├── src/
│   ├── __init__.py
│   ├── data_loader.py            # Loads CSV into Pandas DataFrames and logs ingestion metadata
│   ├── transaction_classifier.py  # Rule-based engine to classify records as 'Expense' or 'Income'
│   ├── trend_analysis.py         # Aggregates financial data by month and overall account tenure
│   ├── llm_call.py               # Connects to OpenAI via LangChain to generate financial insights
│   └── financial_simulator.py    # Simulates future financial scenarios based on historical trends
├── .env.example                  # Template for environment variables
├── .gitignore                    # Ensures sensitive files (.env, venv) are not tracked
├── main.py                       # Orchestrator script managing the core data pipeline
├── requirements.txt              # Project Python dependencies
└── streamlit_app.py              # Main entry point for the Streamlit UI dashboard
```

# 🛠️ Getting Started

Follow these steps to set up and run the application locally on a Windows environment.

## Prerequisites

- Python 3.8 or higher installed
- An active OpenAI API key

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

```dos
.\venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory of the project and add your OpenAI credentials:

```env
OPENAI_API_KEY="your_actual_openai_api_key_here"
```

> **Note:** Ensure your `.env` file is added to `.gitignore` to protect your API keys.

# 💻 Running the Application

To launch the interactive Streamlit web application, execute the following command in your terminal:

```bash
streamlit run streamlit_app.py
```

Once running, open your browser and navigate to the local URL provided in the terminal output (typically `http://localhost:8501`).