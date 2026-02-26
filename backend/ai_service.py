import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables, particularly OPENROUTER_API_KEY from the root .env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize the OpenAI client pointing to OpenRouter
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

MODEL_NAME = "openai/gpt-oss-120b"

def test_ai_connection():
    """Simple test to verify OpenRouter connectivity. Should return '4'."""
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "What is 2+2? Reply with just the number."}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenRouter: {e}")
        return f"Error: {str(e)}"

def chat_with_board_context(user_message: str, current_board: dict) -> dict:
    """
    Sends the user message and current board state to the LLM.
    Expects a JSON response with 'text_response' and optionally 'updated_board'.
    """
    system_prompt = f"""You are an AI assistant managing a Kanban board.
The current board state is provided below as JSON.
If the user asks you to modify the board (e.g., move a card, rename a column, add a card, delete a card), you must provide the ENTIRE updated board state in your response.
If the user is just asking a question or making general conversation, you can leave the updated_board field null.

CURRENT BOARD:
{json.dumps(current_board)}

You MUST respond in valid JSON format ONLY, with the following structure:
{{
  "text_response": "Your conversational reply to the user, explaining what you did.",
  "updated_board": <the complete new board JSON object if modified, or null if no changes>
}}
Do not include any markdown format tags like ```json.
"""

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"}
        )
        response_content = completion.choices[0].message.content.strip()
        # Clean up potential markdown formatting if the model still outputs it
        if response_content.startswith("```json"):
            response_content = response_content[7:]
        if response_content.endswith("```"):
            response_content = response_content[:-3]
        return json.loads(response_content.strip())
    except Exception as e:
        print(f"Error in chat_with_board_context: {e}")
        return {
            "text_response": f"Sorry, I encountered an error: {str(e)}",
            "updated_board": None
        }
