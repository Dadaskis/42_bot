"""Telegram bot handlers for SQL query processing."""

import traceback

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from ai_client import AIQueryGenerator
from database import DatabaseManager

class QueryBot:
    """Telegram bot for handling SQL queries."""
    
    def __init__(self, bot_token: str, query_generator: AIQueryGenerator, db_manager: DatabaseManager):
        """
        Initialize the Telegram bot.
        
        Args:
            bot_token: Telegram bot API token
            query_generator: AI query generator instance
            db_manager: Database manager instance
        """
        self.bot = Bot(token=bot_token)
        self.dp = Dispatcher()
        self.query_generator = query_generator
        self.db_manager = db_manager
        
        # Register handlers
        self.dp.message(Command("start", "help"))(self.send_welcome)
        self.dp.message()(self.handle_message)
    
    async def send_welcome(self, message: Message) -> None:
        """Send welcome message."""
        welcome_text = (
            "👋 Hello! I'm a SQL query bot.\n\n"
            "Send me a question in natural language, and I'll:\n"
            "1. Convert it to an SQL query using AI\n"
            "2. Execute it on the database\n"
            "3. Return the result to you\n\n"
            "Example questions:\n"
            "• How many videos are in the system?\n"
            "• How many videos did creator XYZ post?\n"
            "• How many views did all videos get on a specific date?"
        )
        await message.answer(welcome_text)
    
    async def handle_message(self, message: Message) -> None:
        """Handle incoming messages."""
        if not message.text:
            await message.answer("0")
            return
        
        print(f"User input: {message.text}")
        
        try:
            # Generate SQL query from user input
            sql_query = await self.query_generator.generate_sql_query(message.text)
            print(f"Generated SQL: {sql_query}")
            
            # Execute query
            result = await self.db_manager.execute_query(sql_query)
            
            if result is not None:
                await message.answer(str(result))
            else:
                await message.answer("0")
                
        except Exception as e:
            print(f"Error processing message: {e}")
            traceback.print_exc()
            await message.answer("0")
    
    async def start(self):
        """Start the bot."""
        print("Starting bot...")
        await self.dp.start_polling(self.bot)