I got this set of prompts from Claude to help me in working with Claude Code.

## **Prompt 1: Basic Counter App**

Create a simple Flask web app with a counter. Requirements:

1. Single page with:
   - A title: "The Counting Game"
   - Instructions: "Click the button to count up. But beware what happens at 13..."
   - A display showing the current count (starts at 0)
   - A button labeled "Count Up"

2. When the button is clicked, increment the counter by 1 and update the display

3. Use minimal but clean CSS styling (can be inline or in a style block)

4. The counter should work in-memory for now (will add database later)

5. Include clear comments in the code explaining what each part does for a beginner

6. Set it up so I can run it with `python app.py` and view at localhost:5000
```

---

## **Prompt 2: Add the "Boo!" Feature**
```
Enhance the counter app to add the spooky surprise at 13:

1. When the counter reaches 13:
   - Disable the button (no more counting)
   - Hide or fade out the counter display
   - Show a "BOO! 👻" message in large, playful scary text
   - Display a spooky image below the message

2. For the image:
   - Find and download a fun, family-friendly spooky/Halloween image with Creative Commons or similar permissive licensing
   - Save it in a static/images folder
   - Display it on the page when count hits 13
   - Include attribution in a comment if required by the license

3. Add a "Start Over" button that appears after the "Boo!" to reset the game

4. Make the transition to "Boo!" feel fun with simple CSS animations or transitions
```

---

## **Prompt 3: Add SQLite Database for Game History**
```
Integrate SQLite to track game history:

1. Create a database that stores each completed game with:
   - Game ID (auto-increment primary key)
   - Timestamp when the game reached 13
   - Number of seconds it took to complete (time from first click to reaching 13)

2. Modify the app to:
   - Record start time on first button click
   - Save game data to database when counter reaches 13
   - Show game statistics on the page: "This was game #X. Your fastest game was Y seconds."

3. Add a "View History" section that displays:
   - List of all past games with timestamps and completion times
   - Total number of games played

4. Include the SQL schema in a comment and add comments explaining the database operations for a beginner

5. Ensure the database file persists across app restarts