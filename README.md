# Agent Project

This project uses MLflow and DSPy for AI agent development.

## Setup

1. Create a virtual environment (already done)
2. Install dependencies:
   ```bash
   pip install mlflow dspy-ai python-dotenv openai
   ```

3. Configure your OpenAI API key:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file

## Running the Agent

1. Start MLflow UI in a separate terminal:
   ```bash
   cd c:\357\agent
   C:\357\agent\.venv\Scripts\python.exe -m mlflow ui --port 5000 --backend-store-uri sqlite:///mlruns.db
   ```

2. Open MLflow UI in your browser: http://localhost:5000

3. Run the agent:
   ```bash
   C:\357\agent\.venv\Scripts\python.exe agent.py
   ```

4. View traces in MLflow UI under the "DSPy" experiment

## Usage

```python
import dspy
from config import get_openai_key

# Configure DSPy with OpenAI
lm = dspy.LM(model='openai/gpt-3.5-turbo', api_key=get_openai_key())
dspy.configure(lm=lm)
```

## Project Structure

- `config.py` - Configuration management (reads from .env)
- `.env` - Your environment variables (gitignored)
- `.env.example` - Template for environment variables
- `datamodel.py` - Pydantic models for flights, users, itineraries
- `tools.py` - DSPy tools for flight operations
- `agent.py` - Main DSPy ReAct agent with MLflow tracking
