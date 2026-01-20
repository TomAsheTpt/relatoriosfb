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

`favelabrass/data/favelabrass.db` is SQLite.

- Tables are created as data is imported – schema evolves with real data
- Likely tables: students, events, transactions, instruments, attendance
- **Always check what tables exist before querying** – run `.tables` or query `sqlite_master`

## Workflow

1. Staff update Google Sheets (their source of truth)
2. I export CSVs to `/imports`
3. Claude helps process CSVs into database tables
4. Claude reads database + docs to answer questions, generate reports
5. Outputs go to `/outputs` or get published (GitHub Pages, etc.)

## Key Principles

- Claude reads data, doesn't write to source Sheets
- Database writes happen via explicit import process with validation
- **Verify counts and numbers** – don't trust first-pass generation
- Staff see beautiful outputs, not the plumbing

## Common Tasks

- "Import this CSV into the database"
- "How many students play trumpet?"
- "Generate a report on X"
- "What did we decide about Y?" (searches docs)
- "Create an event summary for Z"

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
