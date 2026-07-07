FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY app ./app
COPY scripts ./scripts
COPY data ./data
COPY docs ./docs
COPY eval ./eval

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -e .

EXPOSE 8501

CMD ["streamlit", "run", "app/agent_dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]