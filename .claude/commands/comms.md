Weekly communications check-in for Favela Brass. Run on Mondays.

User input: $ARGUMENTS

Instructions:

1. **Read all comms files:**
   - `favelabrass/docs/comms/strategy.md` — content pillars, platform roles, voice guidelines
   - `favelabrass/docs/comms/calendar.md` — current 4-week plan
   - `favelabrass/docs/comms/ideas.md` — backlog of content ideas

2. **Fetch Instagram and YouTube data:**
   - Run `python3 favelabrass/scripts/fetch_instagram_posts.py` to refresh IG post data (includes `metric_reach`, `metric_shares`, `metric_saved` per post, plus `account.followers_count`)
   - Run `python3 favelabrass/scripts/fetch_youtube_stats.py` to refresh YouTube channel + video stats
   - Parse `favelabrass/imports/instagram_posts.json` and `favelabrass/imports/youtube_stats.json`
   - Show posts from the past 2 weeks in a table with date, type, likes, comments, reach, and caption snippet
   - This replaces manually asking "what got posted?" (the APIs are the source of truth)

2a. **Show the trend dashboard** (always, at the start of the review):

   **Instagram monthly (current year):**
   | Month | Posts | Total reach | Avg reach/post | Likes | Comments | Shares | Saves |

   Compute from `metric_reach`, `like_count`, `comments_count`, `metric_shares`, `metric_saved`. Flag if avg reach/post is trending down month on month, or if volume dropped below 3/week.

   **Top 5 IG posts by reach (current year):** date, reach, likes, shares, caption snippet.

   **Follower count** from `account.followers_count`.

   **YouTube:** subscribers, total views, video count, plus any uploads in the past 4 weeks with their view counts.

   **Stories:** captured every 4h on the VPS (cron at :47). Query `instagram_stories` on the server DB. Show: count posted in past 14d, total reach, top 3 by reach. Note that very recent stories may have low metrics if captured early in their 24h window.

   Keep this tight (tables, not prose). The point is to spot trends, not narrate them.

3. **Pull context from the database:**
   - Upcoming events in the next 4 weeks: `SELECT name, date, type, location FROM events WHERE date BETWEEN date('now') AND date('now', '+28 days') ORDER BY date;`
   - Recent exam results (if any): `SELECT COUNT(*) as passes FROM assessments WHERE date >= date('now', '-14 days');`
   - Active student count: `SELECT COUNT(*) FROM students WHERE status='Ativo';`
   - Upcoming holidays: `SELECT name, date FROM holidays WHERE date BETWEEN date('now') AND date('now', '+28 days') ORDER BY date;`

4. **Review the past week:**
   Present to Tom:
   - What was planned in the calendar for the period since last review
   - Cross-reference with the Meta API data to see what actually got posted
   - Identify gaps: what was planned but not posted? What got posted that wasn't planned?
   - Ask Tom for context on anything the API can't explain (e.g. why something was skipped)

5. **Surface opportunities:**
   Based on DB data and the ideas backlog, suggest 3-5 specific content ideas for the next 1-2 weeks. Be concrete:
   - Not "post a rehearsal clip" but "Banda Roxa rehearsal on Tuesday — capture 30s of [specific piece] for a reel"
   - Not "student spotlight" but "Maria passed Level 3 last month — short interview about her journey?"
   - Tie ideas to upcoming events, milestones, or seasonal moments

6. **Plan the next 2 weeks:**
   Have a conversation with Tom about:
   - What content can realistically be created this week?
   - Who's capturing? (Tom, Wesley, teacher, volunteer?)
   - Any events or moments worth covering?
   - LinkedIn or newsletter due?
   - One question at a time — Tom may be on voice

7. **Update the files:**
   After agreeing on the plan:
   - Update `calendar.md`:
     - Mark past week items as posted/skipped
     - Roll the calendar forward (remove completed weeks, add new weeks)
     - Update "Last reviewed" and "Next review" dates
   - Update `ideas.md`:
     - Move used ideas to done (check the box)
     - Add any new ideas that came up
     - Move rejected ideas to the Parked section

8. **Quick stats (show at the end):**
   - Posts planned vs posted this week: X/Y
   - Content pillar balance this month (are we overweighting one pillar?)
   - Next big content moment (event, milestone, deadline)

Keep it conversational, one question at a time. This should feel like a 10-minute planning chat, not a reporting exercise.
