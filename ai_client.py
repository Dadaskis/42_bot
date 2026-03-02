"""AI-powered SQL query generator using OpenRouter."""

import traceback

from openai import AsyncOpenAI
from config import OPENROUTER_BASE_URL, DEFAULT_MODEL, EMPTY_QUERY, SYSTEM_PROMPT

class AIQueryGenerator:
    """Handles AI-powered SQL query generation."""
    
    def __init__(self, api_token: str, model: str = DEFAULT_MODEL):
        """
        Initialize the AI query generator.
        
        Args:
            api_token: OpenRouter API token
            model: Model to use for query generation
        """
        self.client = AsyncOpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=api_token,
        )
        self.model = model
    
    async def generate_sql_query(self, user_input: str, max_length: int = 255) -> str:
        """
        Convert natural language to SQL query using AI.
        
        Args:
            user_input: Natural language query from user
            max_length: Maximum length of input to process
            
        Returns:
            SQL query string or empty query on error
        """
        truncated_input = user_input[:max_length]
        
        try:
            completion = await self.client.chat.completions.create(
                extra_body={},
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": truncated_input}
                ]
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating SQL query: {e}")
            traceback.print_exc()
            return EMPTY_QUERY