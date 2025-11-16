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

## Usage

```python
import dspy
from config import get_openai_key

# Configure DSPy with OpenAI
lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key=get_openai_key())
dspy.settings.configure(lm=lm)
```

## Project Structure

- `config.py` - Configuration management (reads from .env)
- `.env` - Your environment variables (gitignored)
- `.env.example` - Template for environment variables
