# AI BIM Intelligence Agent

AI BIM Intelligence Agent is a Python-based project that transforms Revit/BIM room data into structured analytics and extends it with an OpenAI-powered tool-calling agent.

The system can analyze processed BIM room data, answer natural-language questions, detect anomalous rooms using machine learning, and generate BIM quality insights for engineers, project managers, and technical reviewers.

The project demonstrates an enterprise-style LLM agent workflow:

User question → OpenAI tool-calling agent → BIM analytics tools → structured tool output → natural-language answer

## Features

- Revit/BIM room data ingestion and transformation
- Cleaned room data stored as Parquet
- Floor-area analytics
- Largest-room analysis
- Material summary analysis
- Room anomaly detection using Isolation Forest
- OpenAI-powered natural-language BIM assistant
- OpenAI tool-calling agent that selects analytics tools automatically
- Streamlit dashboard for interactive testing
- Debug panel showing selected tools and response time
- Basic evaluation script for tool-selection and answer-quality checks

## Architecture

```text
Revit room export
    ↓
Python ingestion and transformation pipeline
    ↓
Processed Parquet dataset
    ↓
BIM analytics tools
    ↓
OpenAI tool-calling agent
    ↓
Natural-language BIM insights in Streamlit
```

```markdown
## Tech Stack

- Python
- Pandas
- DuckDB
- PyArrow / Parquet
- Scikit-learn
- OpenAI API
- Streamlit
- python-dotenv
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/PatrikEdelenji/revit-bim-project.git
cd revit-bim-project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv1
venv1\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -e .
```

or

```bash
pip install openai python-dotenv streamlit
```

### 4. Configure environment variables

Create a .env file in the project root.

Example:

```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

### 5. Run the BIM data pipeline

```bash
python -m scripts.run_pipeline
```

### 6. Run tests

```bash
python -m scripts.test_ai_tools
python -m scripts.test_agent
python -m scripts.test_openai_agent
python -m scripts.test_openai_tool_agent
```

### 7. Run evaluation

```bash
python -m scripts.evaluate_openai_tool_agent
```

### 8. Start the Streamlit app

```bash
streamlit run app/agent_dashboard.py
```
