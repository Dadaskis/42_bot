"""Main application entry point for the Telegram SQL bot."""

import asyncio
import traceback

from tokens import setup_tokens
from ai_client import AIQueryGenerator
from database import DatabaseManager
from bot import QueryBot
from config import DB_CONFIG

async def main():
    """Main application entry point."""
    
    # Setup tokens
    api_token, bot_token = setup_tokens()
    
    # Initialize components
    query_generator = AIQueryGenerator(api_token)
    db_manager = DatabaseManager(DB_CONFIG)
    
    try:
        # Connect to database
        await db_manager.connect()
        
        # Create and start bot
        bot = QueryBot(bot_token, query_generator, db_manager)
        await bot.start()
        
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
    finally:
        # Cleanup
        await db_manager.close()
        print("Cleanup completed")

if __name__ == "__main__":
    asyncio.run(main())