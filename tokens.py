"""Token management utilities for the Telegram SQL bot."""

from pathlib import Path
from typing import Tuple

def read_token_from_file(file_path: str, placeholder: str = "Put yo' token here.") -> Tuple[str, bool]:
    """
    Read token from file. If file doesn't exist or token is invalid, create file with placeholder.
    
    Args:
        file_path: Path to the token file
        placeholder: Placeholder text to write if file doesn't exist
        
    Returns:
        Tuple of (token, is_valid)
    """
    path = Path(file_path)
    
    try:
        if path.exists():
            token = path.read_text().strip()
            if token and token != placeholder:
                return token, True
        
        # Create file with placeholder if it doesn't exist or token is invalid
        path.write_text(placeholder)
        return "", False
        
    except Exception as e:
        print(f"Error reading token from {file_path}: {e}")
        return "", False

def setup_tokens() -> Tuple[str, str]:
    """Setup and validate both API tokens."""
    
    # Read OpenRouter token
    api_token, api_valid = read_token_from_file("token.txt")
    if not api_valid:
        print("OpenRouter API token is missing or invalid.")
        print("Please add your token to 'token.txt' and restart the bot.")
        quit(1)
    
    # Read Telegram bot token
    bot_token, bot_valid = read_token_from_file("bot_token.txt")
    if not bot_valid:
        print("Telegram Bot API token is missing or invalid.")
        print("Please add your token to 'bot_token.txt' and restart the bot.")
        quit(1)
    
    return api_token, bot_token