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
│   │   └── processed/  # Processed CSVs get moved here
│   ├── docs/           # Markdown: policies, meeting notes, plans
│   │   └── context/    # Deep context files for AI
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
- Wesley – music director
- Raíssa – finances
- Iris – Coda admin / ops support / programme admin
- Lillian – parent & community relations (part-time)
- Wellington – on-site production / logistics (paid per event)
- Plus teachers

**Recently departed:**
- Camila (communications) – fired December 2025
- Carol (events) – left

**Deep Context:** See `favelabrass/docs/context/` for detailed team profiles, project plans, and organizational context.

## Database

`favelabrass/data/favelabrass.db` is SQLite. **This is the source of truth.**

Current tables (Jan 2026):
- `students` - master student list (~250 students)
- `groups` / `group_assignments` - bands and theory class assignments
- `activities` - group activities (rehearsals, workshops)
- `private_lessons` - 1:1 lessons (70 lessons)
- `instruments` / `instrument_loans` - inventory and who has what
- `assessments` - MTB exam results
- `teachers` - staff details, hourly rates
- `student_status_history` - departure log (renamed to Saidas in spreadsheet)

**Always check what tables exist before querying** – run `.tables` or query `sqlite_master`

## Workflow (NEW - Jan 2026)

**SQLite DB is source of truth. Staff interact via Slack bot.**

```
SQLite DB (truth)
    ↑           ↓           ↑
  Slack      Website    Spreadsheet
  (query     (read-     (bulk
  + update)   only)      imports)
```

1. Staff query via Slack: `/aluno 139`, `/banda preta`, `/horario joana`
2. Staff request updates via Slack: `ATUALIZAÇÃO: 139 aula mudar Ter 18:30`
3. Bot confirms or flags conflicts
4. DB updates, Git commits, website regenerates
5. Bulk imports (new students, start-of-year) still via spreadsheet → Tom

**Backup:** Git version control on entire HQ folder. Every DB change = commit. Rollback = `git checkout`.

## Key Principles

- **DB is truth** – not Google Sheets
- **Staff self-serve** via Slack queries
- **Updates require confirmation** – bot proposes, human approves
- **Git protects everything** – any mistake is reversible
- **Website is the output** – timetables, reports, public info

## Common Tasks

- "Import this CSV into the database" (bulk imports)
- "Regenerate the timetable website"
- "How many students play trumpet?"
- "Generate a report on X"
- "What did we decide about Y?" (searches docs)
- "Create an event summary for Z"
- "Process the WhatsApp/Slack updates" (if not using bot)

## Outputs

Generated HTML files in `/outputs`:
- `horarios-2026.html` - Timetable (private lessons + group activities)
- `bandas.html` - Band rosters
- Monthly financial reports
- Annual reports

## Context Files

Key context documents for Claude:

**Favela Brass:**
- `favelabrass/docs/style-guide.md` – **READ THIS before generating any HTML/websites** – colors, typography, brand guidelines
- `favelabrass/docs/context/team-profiles.md` – honest assessments of each team member's strengths, weaknesses, and how to work with them
- `favelabrass/docs/context/tom-role-transition.md` – strategic plan for Tom transitioning from "doing everything" to Artistic Director
- `favelabrass/docs/context/bad-kissingen-project.md` – July 2026 Germany exchange project
- `favelabrass/docs/context/board-governance.md` – governance structure and issues
- `favelabrass/docs/context/location-strategy.md` – the Curvelo opportunity and three-step ladder model for student progression
- `favelabrass/docs/context/data-architecture.md` – database design: tables, relationships, attendance system, assessments, instruments

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
