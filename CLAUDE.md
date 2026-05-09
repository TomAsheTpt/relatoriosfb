# HQ

## What HQ Is

This is my second brain and operational command centre.

- **Obsidian vault** – all markdown files are browsable and editable in Obsidian
- **SQLite database** – holds structured data that needs querying
- **Private** – staff don't see HQ; they work in Google Sheets/Docs, I import their data here

## Folder Structure

```
HQ/
├── CLAUDE.md           # This file – system documentation for Claude
├── favelabrass/        # Favela Brass nonprofit operations
│   ├── data/           # SQLite database lives here
│   │   └── favelabrass.db
│   ├── imports/        # Drop CSVs here for processing
│   │   ├── processed/  # Processed CSVs get moved here
│   │   └── readai/     # Read.ai meeting transcripts (synced from VPS)
│   ├── docs/           # Markdown: policies, meeting notes, plans
│   │   ├── context/    # Deep context files for AI
│   │   └── comms/      # Communications planning (strategy, calendar, ideas)
│   ├── scripts/        # Python scripts for data processing
│   │   ├── generate_timetable.py
│   │   ├── generate_roteiro_admin.py
│   │   ├── assign_rooms.py
│   │   ├── deploy_roteiro.sh
│   │   ├── server_sql.sh          # Run SQL on server DB via SSH
│   │   ├── sync_readai.sh        # Sync meeting transcripts from VPS
│   │   ├── readai_webhook.py     # Webhook receiver (deployed to VPS)
│   │   └── fetch_instagram_posts.py  # Pull all IG posts via Graph API
│   └── outputs/        # Generated reports, dashboards
├── personal/           # Personal notes and context
│   ├── context/        # Tom's profile, GTD protocol, intervention triggers
│   ├── check-ins/      # Weekly check-in records
│   └── diary/          # Personal diary entries
└── projects/           # Other projects
```

## Favela Brass Context

**Associação Musical Favela Brass** – Brazilian music education nonprofit.

- ~250 students across multiple sites
- Teaches brass and percussion to young people in favelas
- Funded by Lei Rouanet (government cultural funding) + donations + performance fees
- Runs on EOS/Traction (quarterly Rocks, weekly L10 meetings)

**Staff:**
- Tom – executive director (founder)
- Wesley – music director
- Raíssa – finances
- Iris – ops support / programme admin
- Lillian – parent & community relations (part-time)
- Edlene – produtora (event logistics/production + assessoria de imprensa), PJ/MEI, started Feb 12 2026, 3-month review May 12 2026
- Wellington – on-site production / logistics (paid per event)
- Plus teachers

**Recently departed:**
- Camila (communications) – fired December 2025
- Carol (events) – left (Edlene replaced her in Feb 2026)

**Deep Context:** See `favelabrass/docs/context/` for detailed team profiles, project plans, and organizational context.

## Database

**The SERVER database (`root@45.55.73.116:/root/favelabrass.db`) is the source of truth.**

The local copy at `favelabrass/data/favelabrass.db` is a read-only cache. It receives writes from the Slack bot, lojinha POS, attendance system, and agenda API. The local copy is synced from the server before generating HTML.

Current tables (Jan 2026):
- `students` - master student list (~250 students)
- `groups` / `group_assignments` - bands and theory class assignments
- `activities` - group activities (rehearsals, workshops)
- `private_lessons` - 1:1 lessons (70 lessons)
- `instruments` / `instrument_loans` - inventory and who has what
- `assessments_practical` / `assessments_theory` - exam results (portal uses these)
- `assessments` - legacy combined exam table (not used by portal)
- `teachers` - staff details, hourly rates
- `student_status_history` - departure log (renamed to Saidas in spreadsheet)
- `events` / `event_staff` / `event_students` - shows, trips, workshops
- `semesters` - academic term dates
- `holidays` - Brazilian public holidays

**For READ queries:** Use `sqlite` MCP (local, read-only) or `sqlite-server` MCP (live server data, no sync needed).
**For WRITE queries:** Use `sqlite-server` MCP `write_query` (requires confirmation) or SSH via `server_sql.sh`.

## Server-First Workflow

**The server DB is the single source of truth.** All services (Slack bot, lojinha, attendance, agenda) write to it. The local DB is a read-only cache that gets synced before HTML generation.

```
   Server DB (truth)  ←── Slack bot, lojinha, attendance, agenda
        ↓ (sync)           ↑ (writes via SSH)
   Local DB (cache)        Claude
        ↓ (read)
   HTML generation → deploy
```

**Rules for Claude:**
1. **READS:** Sync from server first, then use `sqlite` MCP on local DB
2. **WRITES:** Always run SQL on the server via SSH, then sync local
3. **NEVER** write to local DB — `write_query` and `create_table` are denied in settings
4. **NEVER** push the local DB file to the server — it will wipe live data

**Enforced safeguards (not just documentation — actually enforced):**
- MCP sqlite opens local DB in `?mode=ro` (read-only at SQLite level)
- `mcp__sqlite__write_query` and `mcp__sqlite__create_table` are denied in `.claude/settings.local.json`
- Local DB file is chmod 444 (read-only at OS level) after every sync
- All deploy scripts sync via `sync_db.sh` before generating HTML

**How to write to the database:**
```bash
# Single SQL statement
ssh root@45.55.73.116 "sqlite3 /root/favelabrass.db \"UPDATE private_lessons SET teacher='Wesley de Araújo' WHERE id='PL076'\""

# Or use the helper script
./favelabrass/scripts/server_sql.sh "UPDATE private_lessons SET teacher='Wesley de Araújo' WHERE id='PL076'"
```

**How to sync local DB (do this before any reads or HTML generation):**
```bash
./favelabrass/scripts/sync_db.sh
```
This syncs from server, sets chmod 444, and cleans up stale WAL/SHM files.

**All deploy scripts sync from server automatically before generating HTML.**

**Staff workflow:**
1. Staff query via Slack: `/aluno 139`, `/banda preta`, `/horario joana`
2. Staff request updates via Slack: `ATUALIZAÇÃO: 139 aula mudar Ter 18:30`
3. Bot confirms or flags conflicts
4. DB updates, Git commits, website regenerates
5. Bulk imports (new students, start-of-year) still via spreadsheet → Tom

**Claude's direct access (via MCP):**
- `sqlite` → **read-only** queries on local DB cache (sync from server first)
- `sqlite-server` → queries on **live server DB** via SSH tunnel. Reads auto-allowed; writes require confirmation.
- `slack` → read channel history, post messages, check user profiles
- `gdrive` → search Google Drive, read spreadsheets, update cells

**DigitalOcean VPS:** 45.55.73.116
- **Claude has SSH access** - can run commands directly via `ssh root@45.55.73.116 "command"`
- Runs services:
  - `favelabrass-bot` - Slack bot (port 5000)
  - `readai-webhook` - Read.ai transcript receiver (port 5001)
  - `lojinha-web` - Merchandise POS (port 5002)
  - `agenda-api` - Event calendar API (port 5005)

**Portal Auto-Regeneration (cron):**
- Server has its own copy of all generator scripts at `/root/portal-gen/scripts/`
- Cron runs `/root/portal-gen/regenerate.sh` **hourly at :17** — regenerates all portal HTML from the server DB
- Presences auto-deploy runs hourly at :00 via `/root/auto-deploy-presencas.sh`
- Google Calendar sync runs **hourly at :30** via `/root/sync_google_calendar.py` — pushes DB events (shows/festivals/trips only, excluding cancelled) to the "Apresentações Favela Brass" calendar. Log: `/var/log/gcal-sync.log`. When editing `favelabrass/scripts/sync_google_calendar.py` locally, `scp` to `/root/sync_google_calendar.py`.
- Instagram fetch runs **every 4h at :47** via `/root/fetch_instagram_posts.py`. Captures live Stories before the 24h window expires (writes to `instagram_stories` and `instagram_account_snapshots`), and refreshes posts. Log: `/var/log/ig-fetch.log`. Token at `/root/.config/fab-ia/ig_token.txt`. When editing `favelabrass/scripts/fetch_instagram_posts.py` locally, `scp` to `/root/fetch_instagram_posts.py`.
- **CRITICAL:** When fixing a generator script locally, you MUST also update the server copy at `/root/portal-gen/scripts/<script>.py` — otherwise the cron will overwrite your HTML fix within the hour
- Uploading only the HTML output is a temporary fix that will be reverted by the next cron run

**Slack Bot:**
- Local code: `/Users/tom/Documents/favelabrass-bot/`
- Server code: `/root/app.py`, `/root/favelabrass.db`

**Read.ai Webhook:**
- Local code: `favelabrass/scripts/readai_webhook.py`
- Server code: `/root/readai_webhook.py`
- Transcripts save to: `/root/readai-imports/`

**Deploy commands:**
```bash
# Deploy Slack bot
scp /Users/tom/Documents/favelabrass-bot/app.py root@45.55.73.116:/root/
ssh root@45.55.73.116 "systemctl restart favelabrass-bot"

# Deploy Read.ai webhook
scp favelabrass/scripts/readai_webhook.py root@45.55.73.116:/root/
ssh root@45.55.73.116 "systemctl restart readai-webhook"

# Check service status/logs
ssh root@45.55.73.116 "systemctl status favelabrass-bot"
ssh root@45.55.73.116 "systemctl status readai-webhook"
ssh root@45.55.73.116 "journalctl -u favelabrass-bot -n 50"
ssh root@45.55.73.116 "journalctl -u readai-webhook -n 50"
```

**DigitalOcean Console:** https://cloud.digitalocean.com/droplets (password in 1Password)

**Backup:** Git version control on entire HQ folder. Every DB change = commit. Rollback = `git checkout`.

## Session Startup

At the start of each session:

**1. Sync the database from the server:**
```bash
./favelabrass/scripts/sync_db.sh
```

**2. Check for unread staff feedback:**
```sql
SELECT slack_user_name, content, datetime(received_at, 'localtime') FROM feedback WHERE status = 'unread' ORDER BY received_at
```

If there's feedback, summarise it for Tom and propose a plan. After actioning, mark it done via `sqlite-server` MCP:
```sql
UPDATE feedback SET status = 'actioned', actioned_at = datetime('now'), actioned_notes = 'Description of what was done' WHERE status = 'unread'
```

## Key Principles

- **Server DB is truth** – writes go via `sqlite-server` MCP or SSH; local is a locked read-only cache
- **Staff self-serve** via Slack queries
- **Updates require confirmation** – bot proposes, human approves
- **Git protects everything** – any mistake is reversible
- **Website is the output** – timetables, reports, public info
- **Investigate before messaging staff** – when data looks wrong, check server logs (`journalctl -u <service>`) and recent actions before contacting anyone. Consider whether Claude caused the problem.
- **Keep context files current** – when a session changes how something works (database schema, workflows, tools, processes), update the relevant context files in `favelabrass/docs/context/`, `CLAUDE.md`, and memory before closing out. Stale docs cause wrong decisions in future sessions.

## Read.ai Meeting Transcripts

Meetings recorded via Read.ai automatically save transcripts to the VPS.

**Sync transcripts locally:**
```bash
./favelabrass/scripts/sync_readai.sh
```
Transcripts land in `favelabrass/imports/readai/`

**Process a meeting (extract decisions → context files):**
```bash
/process-meeting <filename>
```
This reads the transcript, extracts decisions, and routes them to the appropriate context file (eos-planning.md, team-profiles.md, etc.).

## Common Tasks

- "Import this CSV into the database" → bulk imports via scripts, write to server via `sqlite-server` MCP
- "Regenerate the timetable website" → run deploy script (auto-syncs from server)
- "How many students play trumpet?" → `sqlite-server` MCP: `SELECT ... FROM students`
- "Generate a report on X" → `sqlite-server` MCP for data, then format output
- "What did we decide about Y?" → search docs/ with Grep, or check meeting transcripts
- "Create an event summary for Z" → `sqlite-server` MCP for event data
- "Pull Raíssa's latest spreadsheet" → `gdrive` MCP: search + read Google Sheets directly
- "Check what staff are saying" → `slack` MCP: read channel history
- "Post an update to Slack" → `slack` MCP: post message (always confirm with Tom first)
- "Sync and process meeting transcripts" → Read.ai → context files
- "Client wants a proposal for a gig" → `/proposta` (single-page branded PDF, ledger tracked)

## Outputs

Generated HTML files in `/outputs`:
- `central.html` - Staff portal / central hub (links to all other sites)
- `horarios-2026.html` - Timetable (private lessons + group activities)
- `presencas-2026.html` - Attendance tracking site (password-protected)
- `roteiro-admin.html` - Timetable admin (Iris self-service: lessons, activities, groups, theory)
- `bandas.html` - Band rosters
- `agenda.html` - Event calendar overview
- `bad-kissingen-2026.html` - Individual event production pages
- Monthly financial reports
- Annual reports

**Live Sites:**
- `central.favelabrass.org` - Staff portal / central hub (GitHub Pages, repo: TomAsheTpt/central)
- `roteiro.favelabrass.org` - Internal timetable (GitHub Pages, repo: TomAsheTpt/roteiro)
- Attendance tracking is on the portal: `portal.favelabrass.org/presencas.html` (presencas.favelabrass.org GitHub Pages site was removed — HTTPS/HTTP mixed content broke API calls)
- `slack.favelabrass.org` - Personalized Slack guides per role (GitHub Pages, repo: TomAsheTpt/slack-favelabrass)
- `agenda.favelabrass.org` - Event calendar (planned)

**DNS:** favelabrass.org is hosted on WordPress. Add CNAME records there for subdomains → `tomashetpt.github.io`.

**Deploy commands:**
```bash
# Regenerate staff portal and deploy to central.favelabrass.org
./favelabrass/scripts/deploy_central.sh

# Regenerate timetable and deploy to roteiro.favelabrass.org
./favelabrass/scripts/deploy_roteiro.sh

# Regenerate attendance site and deploy to portal VPS
./favelabrass/scripts/deploy_presencas.sh

# Just regenerate HTML locally
python3 favelabrass/scripts/generate_timetable.py
python3 favelabrass/scripts/generate_attendance.py

# Auto-assign rooms (run before generate if room assignments changed)
python3 favelabrass/scripts/assign_rooms.py

# Generate timetable admin page
python3 favelabrass/scripts/generate_roteiro_admin.py

# Generate event calendar and individual event pages
python3 favelabrass/scripts/generate_calendar.py
python3 favelabrass/scripts/generate_event_page.py favelabrass/events/bad-kissingen-2026

# Sync event sheets from Google Drive (requires env vars)
python3 favelabrass/scripts/sync_event_sheets.py
```

## Browser Automation (Playwright)

Playwright (Python) is installed via pipx at `~/.local/bin/playwright`. All three browser engines (Chromium, Firefox, WebKit) are available.

**When to use it:**
- Verifying generated HTML pages render correctly after deployment
- Scraping data from sites that require JavaScript (Google Sheets published pages, etc.)
- Taking screenshots of live sites for reports or debugging
- Automating form submissions or interactions that can't be done via API

**Quick usage:**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    # page.screenshot(path="screenshot.png")
    browser.close()
```

**Note:** To use in scripts, run them with the pipx venv Python: `~/.local/pipx/venvs/playwright/bin/python script.py`

## MCP Servers

Configured in `.mcp.json` (Claude Code) and `~/Library/Application Support/Claude/claude_desktop_config.json` (Claude Desktop).

**Active servers:**

| Server | Package | What it does |
|--------|---------|--------------|
| `sqlite` | `mcp-server-sqlite-npx` | **Read-only** access to local DB cache. Fast, no network. Sync first via `sync_db.sh`. |
| `sqlite-server` | `mcp-server-sqlite-npx` via SSH | **Live server DB**. Reads auto-allowed; writes require confirmation. No sync needed. |
| `slack` | `@modelcontextprotocol/server-slack` | Read channels, post messages, get user profiles. Uses existing bot token. |
| `gdrive` | `mcp-gdrive` | Search Google Drive, read files, read/write Google Sheets. OAuth creds in `~/.config/mcp-gdrive/`. |

**Not yet configured:**
- `github` – needs PAT from `gh auth login`. Will add when Tom authenticates.

**When to use which:**
- **Need to query student data, timetables, attendance?** → `sqlite-server` MCP (live) or `sqlite` MCP (local, sync first)
- **Need to write to the database?** → `sqlite-server` MCP `write_query` (prompts for confirmation)
- **Need to check Slack messages or post updates?** → `slack` MCP
- **Need to read Raíssa's spreadsheets or event sheets?** → `gdrive` MCP
- **Need to deploy to GitHub Pages?** → Use `gh` CLI for now (no MCP yet)

**First-time auth for Google Drive:** The first time `gdrive` is used, it will open a browser window for Google OAuth consent. Approve it once, then it caches the token in `~/.config/mcp-gdrive/`.

## Context Files

Key context documents for Claude:

**Favela Brass:**
- `favelabrass/docs/style-guide.md` – **READ THIS before generating any HTML/websites** – colors, typography, brand guidelines
- `favelabrass/docs/context/eos-planning.md` – **EOS/Traction data**: V/TO, core values, 10yr/3yr/1yr goals, SWOT, Issues List, quarterly Rocks, Scorecard, team promises
- `favelabrass/docs/context/team-profiles.md` – honest assessments of each team member's strengths, weaknesses, and how to work with them
- `favelabrass/docs/context/tom-role-transition.md` – strategic plan for Tom transitioning from "doing everything" to Artistic Director
- `favelabrass/docs/context/bad-kissingen-project.md` – July 2026 Germany exchange project
- `favelabrass/docs/context/board-governance.md` – governance structure and issues
- `favelabrass/docs/context/location-strategy.md` – the Curvelo opportunity and three-step ladder model for student progression
- `favelabrass/docs/context/data-architecture.md` – database design: tables, relationships, attendance system, assessments, instruments
- `favelabrass/docs/rouanet/pronac-254750-2026.md` – **2026 Rouanet project**: approved targets (272 student places, 39 shows), budget (R$2.36M), captação status, product breakdown
- `favelabrass/docs/context/captacao-strategy.md` – **Captação strategy 2026**: two-pipeline plan (corporate + PF Rouanet), planned Coordenador(a) de Desenvolvimento Institucional hire, OSESP-modelled PF tier ladder co-led by Margo Black, sequencing May–Dec 2026
- `favelabrass/docs/context/slack-bot-spec.md` – Slack bot commands, role-based access, `/pergunta` natural language queries
- `favelabrass/docs/context/event-sheets-setup.md` – Google Sheets → DB sync for event production pages
- `favelabrass/docs/context/manual-2026.md` – Student/parent manual with attendance policies, thresholds, band progression rules

**Communications:**
- `favelabrass/docs/comms/strategy.md` – Content pillars, platform roles, voice/tone, posting cadence, delegation plan
- `favelabrass/docs/comms/calendar.md` – Rolling 4-week content plan (reviewed Mondays via `/comms`)
- `favelabrass/docs/comms/ideas.md` – Content ideas backlog
- `favelabrass/docs/comms/social-insights.md` – **READ THIS for content decisions** – cross-platform performance data (Instagram + YouTube), what works per channel, what doesn't
- `favelabrass/docs/comms/caption-style-guide.md` – **READ THIS before writing any Instagram caption** – voice, structure, emoji, hashtag, and accessibility patterns derived from 863 real posts. Use `/caption` command to draft captions.

**Personal:**
- `personal/context/tom-profile.md` – Complete profile: Twatometer, patterns, daily routine, what matters to Tom
- `personal/context/gtd-protocol.md` – Friday morning weekly check-in system and GTD review protocol
- `personal/context/intervention-protocol.md` – AI intervention triggers for operational drift and side project proliferation
- `personal/check-ins/` – Weekly check-in records (most recent + archive)
- `personal/diary/complete_diary.md` – Personal diary entries

## Working with Tom

- British, direct, no sugar-coating
- Prefers concise responses
- Values honest disagreement over false validation
- Mornings are sacred creative time (arranging, practice) - no meetings before 12:00
- Currently transitioning away from operational work toward artistic/strategic focus
- Frustrated by: wordy writing, incomplete projects, people who can't work independently, things landing back on his plate

## Tone & Communication

- Write with dry British wit – understated, self-deprecating, occasionally sarcastic
- Favour deadpan delivery over exclamation marks
- When things go wrong, respond with resigned acceptance rather than alarm ("Well, that's gone spectacularly sideways")
- Understatement is preferred ("bit of a faff" over "major problem")
- Avoid American corporate enthusiasm – no "awesome", "super excited", or "let's crush it"
- Tea references acceptable but not mandatory
