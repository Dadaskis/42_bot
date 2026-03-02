# 42_bot - Telegram SQL Query Bot

A Telegram bot that converts natural language questions into SQL queries using AI and returns numerical answers from a PostgreSQL database containing video statistics data.

## Features

- Natural language processing for database queries in Russian
- AI-powered SQL query generation using OpenRouter API
- Asynchronous architecture with aiogram and asyncpg
- PostgreSQL database with video statistics and hourly snapshots
- Returns single numerical answers as specified in requirements

## Technology Stack

- Python 3.8+
- PostgreSQL
- aiogram (async Telegram bot framework)
- asyncpg (async PostgreSQL driver)
- OpenRouter API (LLM integration)

## Project Structure

```
├── main.py                 # Application entry point
├── bot.py                  # Telegram bot handlers
├── database.py             # Database connection manager
├── ai_client.py            # AI query generator
├── config.py               # Configuration constants
├── tokens.py               # Token management utilities
├── _turn_JSON_to_pSQL.py   # JSON data import script
├── token.txt               # OpenRouter API token (create this)
├── bot_token.txt           # Telegram bot token (create this)
└── videos.json             # Input data file
```

## Database Schema

### videos table
- `id` (VARCHAR(36)) - Video identifier
- `creator_id` (VARCHAR(36)) - Creator identifier
- `video_created_at` (TIMESTAMPTZ) - Publication timestamp
- `views_count`, `likes_count`, `comments_count`, `reports_count` (INTEGER) - Final counts
- `created_at`, `updated_at` (TIMESTAMPTZ) - Timestamps

### video_snapshots table
- `id` (VARCHAR(36)) - Snapshot identifier
- `video_id` (VARCHAR(36)) - Reference to videos table
- Current values: `views_count`, `likes_count`, `comments_count`, `reports_count` (INTEGER)
- Deltas: `delta_views_count`, `delta_likes_count`, `delta_comments_count`, `delta_reports_count` (INTEGER)
- `created_at`, `updated_at` (TIMESTAMPTZ) - Timestamps

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- PostgreSQL server
- OpenRouter API key
- Telegram bot token (from @BotFather)

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Database Setup

1. Create a PostgreSQL database:
   ```sql
   CREATE DATABASE 42bot_data;
   ```

2. Create a read-only user:
   ```sql
   CREATE USER readonly WITH PASSWORD '1337';
   GRANT CONNECT ON DATABASE 42bot_data TO readonly;
   ```

3. Import the JSON data:
   ```
   python _turn_JSON_to_pSQL.py
   ```

4. Grant a read-only user the needed rights to operate:
    ```sql
    GRANT USAGE ON SCHEMA public TO readonly;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
    ```

### Token Configuration

1. Create `token.txt` and add your OpenRouter API key.

2. Create `bot_token.txt` and add your Telegram bot token.

### Running the Bot

Start the bot with:
```
python main.py
```

## Architecture Overview

### Natural Language to SQL Conversion

The bot uses a two-step approach to convert natural language to database queries:

1. **LLM-based Query Generation**: User input is sent to an LLM (via OpenRouter) with a carefully crafted system prompt that describes the database schema and query requirements. The model is instructed to output only SQL queries.

2. **Query Execution**: Generated SQL is executed on the database using an async connection pool, and the first numerical result is returned to the user.

### System Prompt Design

The system prompt includes:
- Complete table schemas with example rows
- Strict instructions to output only SQL queries
- Handling of irrelevant queries (returns empty result set)
- Support for multiple languages

### Security Considerations

- Read-only database user for query execution
- Input truncation to prevent prompt injection
- No context storage between queries
- Error handling that returns "0" on failures

## Query Examples

The bot can handle questions like:
- "How many videos are in the system?"
- "How many videos does creator XYZ have?"
- "How many videos had more than 100,000 views?"
- "What was the total view growth on November 28, 2025?"
- "How many different videos received new views on November 27, 2025?"

## Error Handling

- Invalid or unrelated questions return "0"
- Database connection issues return "0"
- LLM API failures return "0"
- Malformed SQL queries return "0"

## Configuration Options

Edit `config.py` to modify:
- OpenRouter base URL
- LLM model selection
- Database connection parameters
- System prompt

## Performance Considerations

- Asynchronous operations throughout
- Connection pooling for database access
- Input truncation for API efficiency
- No conversation state maintenance

## License
MIT License! Happiness to everyone.