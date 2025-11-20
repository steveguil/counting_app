# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask web application called "The Counting Game" - an interactive counting game with an easter egg at count 13. The app uses in-memory storage with thread-safe counter operations.

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
- **No database** - Counter stored in global `counter` dict with thread-safe `threading.Lock`

### Request Flow
1. Client loads `/` → Flask renders [templates/index.html](templates/index.html) with initial count
2. User clicks "Count Up" → JavaScript POSTs to `/count`
3. [app.py:41-54](app.py#L41-L54) increments counter with lock, returns JSON
4. Client updates DOM without page reload
5. At count=13 → Modal appears, reset triggered via POST to `/reset`

### Thread Safety
Counter modifications use `counter_lock` (threading.Lock) to prevent race conditions during concurrent requests. Read operations don't require locks in this simple implementation.

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
