# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask web application called "The Counting Game" - an interactive counting game with an easter egg at count 13. The app uses SQLite for persistent storage with thread-safe counter operations.

## Development Commands

### Running the Application
```bash
python app.py
```
The app runs on http://localhost:5000

### Virtual Environment
The project uses a Python virtual environment located at `.venv/`:
```bash
# Activate virtual environment (if needed)
source .venv/bin/activate  # macOS/Linux
```

### Dependencies
```bash
pip install -r requirements.txt
```
Only dependency: Flask>=2.0

## Architecture

### Application Structure
- **Single-file Flask app** ([app.py](app.py)) - All backend logic in one file
- **Single-page frontend** ([templates/index.html](templates/index.html)) - UI with embedded CSS and JavaScript
- **SQLite database** - Counter persisted in `counting_game.db` with thread-safe operations

### Request Flow
1. Client loads `/` → Flask calls `get_counter()` and renders [templates/index.html](templates/index.html) with current count from database
2. User clicks "Count Up" → JavaScript POSTs to `/count`
3. `increment_counter()` atomically updates database with lock, returns new value as JSON
4. Client updates DOM without page reload
5. At count=13 → Modal appears, reset triggered via POST to `/reset` which calls `reset_counter()`

### Database Schema
```sql
CREATE TABLE counter (
    id INTEGER PRIMARY KEY,
    value INTEGER NOT NULL DEFAULT 0
)
```
Single row with `id=1` stores the current counter value.

### Thread Safety
Database modifications use `db_lock` (threading.Lock) to prevent race conditions during concurrent requests. Each database function opens its own connection and closes it when done (SQLite connections are not thread-safe).

### Key Endpoints
- `GET /` - Main UI (renders template with current count)
- `POST /count` - Increment and return new value
- `POST /reset` - Reset counter to 0
- `GET /hello` - Hello World test endpoint

### Frontend Architecture
- **Vanilla JavaScript** with Fetch API (no frameworks)
- **Inline CSS** using CSS variables for theming
- **Modal system** for the "13" easter egg (in-page overlay, not browser alert)
- **State management** handled entirely by server; client just reflects server state

### Database Persistence
- Counter value persists across server restarts
- Database file: `counting_game.db` (created automatically on first run)
- Database is initialized via `init_db()` when app starts ([app.py:29-51](app.py#L29-L51))
- Add `counting_game.db` to `.gitignore` to avoid committing local database state
