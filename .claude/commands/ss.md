Log an SS (Simple & Sinister) training session and show stats.

User input: $ARGUMENTS

Instructions:
1. Parse the user input. Examples:
   - "1-arm" or "2-arm" → full session with that swing type, same weights as last session
   - "1-arm 16/24/24/24/16" → full session with specified weights
   - "no" or "rest" → rest day (no session)
   - Empty → assume full session, 1-arm, same weights as last session

2. Get the last session's weights from the database:
   ```
   sqlite3 /Users/tom/Documents/HQ/personal/data/personal.db "SELECT set_1_kg, set_2_kg, set_3_kg, set_4_kg, set_5_kg FROM ss_training WHERE full_session = 'Y' ORDER BY date DESC LIMIT 1;"
   ```

3. Insert today's record into the ss_training table in /Users/tom/Documents/HQ/personal/data/personal.db

4. After logging, query and display:
   - Confirmation of what was logged
   - Last 7 days: sessions count and percentage
   - Current streak (consecutive days with sessions)
   - Total sessions / total days tracked
