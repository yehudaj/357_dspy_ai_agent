"""Example script showing how to use DSPy with OpenAI."""
import dspy
from config import get_openai_key

# Configure DSPy with OpenAI
lm = dspy.LM(model='openai/gpt-3.5-turbo', api_key=get_openai_key())
dspy.configure(lm=lm)

# Example: Simple question answering
class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")

# Create a predictor
generate_answer = dspy.Predict(BasicQA)

# Example usage
if __name__ == "__main__":
    # Test the setup
    response = generate_answer(question="What is the capital of France?")
    print(f"Question: What is the capital of France?")
    print(f"Answer: {response.answer}")
