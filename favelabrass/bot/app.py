"""
Favela Brass Slack Bot

Staff interface for querying the SQLite database.
Run locally with: python app.py
"""

import os
import sqlite3
import json
from datetime import date
from pathlib import Path
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Database path (relative to this file)
DB_PATH = Path(__file__).parent.parent / "data" / "favelabrass.db"


def get_db():
    """Get database connection."""
    return sqlite3.connect(DB_PATH)


def search_students(query):
    """Search students by ID or name."""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Try as ID first
    if query.isdigit():
        cur.execute("""
            SELECT s.id, s.name, s.status,
                   ga.group_id, g.name as banda,
                   ga.current_instrument, ga.theory_class,
                   pl.teacher as aula_prof, pl.day_of_week as aula_dia,
                   pl.start_time as aula_hora, pl.location as aula_local,
                   il.instrument_id as emprestimo_id
            FROM students s
            LEFT JOIN group_assignments ga ON s.id = ga.student_id
            LEFT JOIN groups g ON ga.group_id = g.id
            LEFT JOIN private_lessons pl ON s.id = pl.student_id AND pl.active = 1
            LEFT JOIN instrument_loans il ON s.id = il.student_id AND il.status = 'Active'
            WHERE s.id = ?
        """, (query,))
        rows = cur.fetchall()
        conn.close()
        return rows

    # Search by name
    cur.execute("""
        SELECT s.id, s.name, s.status,
               g.name as banda,
               ga.current_instrument
        FROM students s
        LEFT JOIN group_assignments ga ON s.id = ga.student_id
        LEFT JOIN groups g ON ga.group_id = g.id
        WHERE s.name LIKE ? AND s.status = 'Ativo'
        ORDER BY s.name
        LIMIT 15
    """, (f"%{query}%",))
    rows = cur.fetchall()
    conn.close()
    return rows


@app.command("/aluno")
def handle_aluno(ack, respond, command):
    """Handle /aluno command - search for student by ID or name."""
    ack()

    query = command["text"].strip()
    if not query:
        respond("Uso: `/aluno <id ou nome>`\nExemplo: `/aluno 139` ou `/aluno maria`")
        return

    rows = search_students(query)

    if not rows:
        respond(f"Nenhum aluno encontrado para \"{query}\"")
        return

    # Single result with full details
    if query.isdigit() and rows:
        r = rows[0]
        lines = [f"*{r['name']}* ({r['id']})"]

        if r['banda']:
            instrument = r['current_instrument'] or "?"
            lines.append(f":musical_note: {r['banda']} | {instrument}")

        if r['theory_class']:
            lines.append(f":books: {r['theory_class']}")

        if r['aula_prof']:
            time_str = r['aula_hora'][:5] if r['aula_hora'] else "?"
            lines.append(f":musical_keyboard: Aula: {r['aula_prof']}, {r['aula_dia']} {time_str} {r['aula_local'] or ''}")

        if r['emprestimo_id']:
            lines.append(f":trumpet: Empréstimo: {r['emprestimo_id']}")

        respond("\n".join(lines))
        return

    # Multiple results
    if len(rows) == 1:
        r = rows[0]
        banda = r['banda'] or "Sem banda"
        instrument = r['current_instrument'] or ""
        respond(f"*{r['name']}* ({r['id']}) - {banda} {instrument}")
        return

    lines = [f"{len(rows)} resultados para \"{query}\":"]
    for r in rows:
        banda = r['banda'] or "Sem banda"
        instrument = r['current_instrument'] or ""
        lines.append(f"  {r['id']} {r['name']} - {banda} {instrument}")

    respond("\n".join(lines))


@app.command("/banda")
def handle_banda(ack, respond, command):
    """Handle /banda command - list students in a band."""
    ack()

    query = command["text"].strip().lower()
    if not query:
        respond("Uso: `/banda <nome>`\nExemplo: `/banda preta`")
        return

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Find the band
    cur.execute("""
        SELECT g.id, g.name,
               COUNT(ga.student_id) as count
        FROM groups g
        LEFT JOIN group_assignments ga ON g.id = ga.group_id
        LEFT JOIN students s ON ga.student_id = s.id AND s.status = 'Ativo'
        WHERE LOWER(g.name) LIKE ?
        GROUP BY g.id
    """, (f"%{query}%",))

    band = cur.fetchone()
    if not band:
        respond(f"Banda não encontrada: \"{query}\"")
        conn.close()
        return

    # Get students grouped by instrument family
    cur.execute("""
        SELECT s.name, ga.current_instrument
        FROM students s
        JOIN group_assignments ga ON s.id = ga.student_id
        WHERE ga.group_id = ? AND s.status = 'Ativo'
        ORDER BY ga.current_instrument, s.name
    """, (band['id'],))

    students = cur.fetchall()
    conn.close()

    # Group by instrument family
    families = {
        'Trompetes': [],
        'Trombones': [],
        'Saxofones': [],
        'Percussão': [],
        'Outros': []
    }

    for s in students:
        inst = (s['current_instrument'] or '').lower()
        name = s['name'].split()[0]  # First name only

        if 'trompete' in inst or 'trumpet' in inst:
            families['Trompetes'].append(name)
        elif 'trombone' in inst:
            families['Trombones'].append(name)
        elif 'sax' in inst:
            families['Saxofones'].append(name)
        elif any(p in inst for p in ['percussão', 'surdo', 'caixa', 'bateria']):
            families['Percussão'].append(name)
        else:
            families['Outros'].append(name)

    lines = [f":saxophone: *{band['name']}* ({len(students)} alunos)\n"]

    for family, names in families.items():
        if names:
            lines.append(f"*{family}* ({len(names)}): {', '.join(names)}")

    respond("\n".join(lines))


@app.command("/horario")
def handle_horario(ack, respond, command):
    """Handle /horario command - show teacher's schedule."""
    ack()

    parts = command["text"].strip().split()
    if not parts:
        respond("Uso: `/horario <professor> [dia]`\nExemplo: `/horario joana` ou `/horario shanso sabado`")
        return

    teacher_query = parts[0].lower()
    day_filter = parts[1].lower() if len(parts) > 1 else None

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Build query
    sql = """
        SELECT pl.day_of_week, pl.start_time, pl.location,
               s.name as student_name, pl.duration_minutes
        FROM private_lessons pl
        JOIN students s ON pl.student_id = s.id
        WHERE LOWER(pl.teacher) LIKE ? AND pl.active = 1
    """
    params = [f"%{teacher_query}%"]

    if day_filter:
        # Map Portuguese day names
        day_map = {
            'seg': 'Segunda', 'segunda': 'Segunda',
            'ter': 'Terça', 'terca': 'Terça',
            'qua': 'Quarta', 'quarta': 'Quarta',
            'qui': 'Quinta', 'quinta': 'Quinta',
            'sex': 'Sexta', 'sexta': 'Sexta',
            'sab': 'Sábado', 'sabado': 'Sábado',
            'dom': 'Domingo', 'domingo': 'Domingo'
        }
        day_name = day_map.get(day_filter, day_filter.title())
        sql += " AND pl.day_of_week = ?"
        params.append(day_name)

    sql += " ORDER BY pl.day_of_week, pl.start_time"

    cur.execute(sql, params)
    lessons = cur.fetchall()
    conn.close()

    if not lessons:
        respond(f"Nenhuma aula encontrada para \"{teacher_query}\"")
        return

    # Get teacher name from first result
    cur = get_db().cursor()
    cur.execute("SELECT DISTINCT teacher FROM private_lessons WHERE LOWER(teacher) LIKE ?", (f"%{teacher_query}%",))
    teacher_name = cur.fetchone()[0]

    # Group by day and location
    by_day = {}
    for l in lessons:
        day = l['day_of_week']
        if day not in by_day:
            by_day[day] = []
        by_day[day].append(l)

    lines = [f":musical_keyboard: *{teacher_name}* - {len(lessons)} aulas\n"]

    # Sort days in order (handles both "Segunda" and "2a - Segunda" formats)
    day_order = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    for day in sorted(by_day.keys(), key=lambda d: next((i for i, x in enumerate(day_order) if x in d), 99)):
            day_lessons = by_day[day]
            location = day_lessons[0]['location'] or ''
            lines.append(f"*{day}* ({location}):")
            for l in day_lessons:
                time = l['start_time'][:5] if l['start_time'] else '?'
                lines.append(f"  {time} {l['student_name'].split()[0]}")
            lines.append("")

    respond("\n".join(lines))


@app.command("/presenca")
def handle_presenca(ack, respond, command):
    """Handle /presenca command - show attendance form for a band or activity."""
    ack()

    query = command["text"].strip().lower()
    if not query:
        respond("Uso: `/presenca <banda>`\nExemplo: `/presenca preta`")
        return

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Find the band
    cur.execute("""
        SELECT g.id, g.name
        FROM groups g
        WHERE LOWER(g.name) LIKE ?
    """, (f"%{query}%",))

    band = cur.fetchone()
    if not band:
        respond(f"Banda não encontrada: \"{query}\"")
        conn.close()
        return

    # Get active students in this band
    cur.execute("""
        SELECT s.id, s.name
        FROM students s
        JOIN group_assignments ga ON s.id = ga.student_id
        WHERE ga.group_id = ? AND s.status = 'Ativo'
        ORDER BY s.name
    """, (band['id'],))

    students = cur.fetchall()
    conn.close()

    if not students:
        respond(f"Nenhum aluno ativo na {band['name']}")
        return

    today = date.today().isoformat()

    # Check existing attendance for today
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT student_id, status FROM attendance
        WHERE date = ? AND activity_type = 'banda' AND activity_name = ?
    """, (today, band['name']))
    existing = {row['student_id']: row['status'] for row in cur.fetchall()}
    conn.close()

    # Build checkboxes - pre-check those already marked present
    options = []
    initial_options = []
    for s in students:
        option = {
            "text": {"type": "plain_text", "text": s['name'].split()[0]},  # First name
            "value": str(s['id'])
        }
        options.append(option)
        # Pre-select if already marked present, or if no record yet (assume present by default)
        if existing.get(s['id']) == 'presente' or s['id'] not in existing:
            initial_options.append(option)

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"📋 {band['name']} - {today}"}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Desmarque os alunos que *faltaram*:"}
        },
        {
            "type": "actions",
            "block_id": f"attendance_{band['name']}_{today}",
            "elements": [
                {
                    "type": "checkboxes",
                    "action_id": "attendance_checkboxes",
                    "options": options,
                    "initial_options": initial_options if initial_options else None
                }
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "💾 Salvar"},
                    "style": "primary",
                    "action_id": "save_attendance",
                    "value": json.dumps({
                        "band": band['name'],
                        "date": today,
                        "student_ids": [s['id'] for s in students]
                    })
                }
            ]
        }
    ]

    # Remove None from initial_options if empty
    if not initial_options:
        blocks[2]["elements"][0].pop("initial_options", None)

    respond(blocks=blocks)


@app.command("/presenca-aula")
def handle_presenca_aula(ack, respond, command):
    """Handle /presenca-aula command - attendance for private lessons."""
    ack()

    parts = command["text"].strip().split()
    if not parts:
        respond("Uso: `/presenca-aula <professor>` ou `/presenca-aula <professor> <dia>`\nExemplo: `/presenca-aula joana` ou `/presenca-aula joana 19`")
        return

    teacher_query = parts[0].lower()

    # Determine date - today or specified day of month
    if len(parts) > 1 and parts[1].isdigit():
        day_num = int(parts[1])
        today = date.today()
        try:
            target_date = today.replace(day=day_num)
        except ValueError:
            respond(f"Dia inválido: {day_num}")
            return
    else:
        target_date = date.today()

    # Map weekday to Portuguese
    day_names = ['2a - Segunda', '3a - Terça', '4a - Quarta', '5a - Quinta', '6a - Sexta', 'Sábado', 'Domingo']
    target_day = day_names[target_date.weekday()]

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get lessons for this teacher on this day of week
    cur.execute("""
        SELECT pl.id as lesson_id, pl.student_id, s.name as student_name,
               pl.start_time, pl.teacher
        FROM private_lessons pl
        JOIN students s ON pl.student_id = s.id
        WHERE LOWER(pl.teacher) LIKE ? AND pl.day_of_week = ? AND pl.active = 1
        ORDER BY pl.start_time
    """, (f"%{teacher_query}%", target_day))

    lessons = cur.fetchall()

    if not lessons:
        # Try without the "2a - " prefix
        simple_day = target_day.split(' - ')[-1] if ' - ' in target_day else target_day
        cur.execute("""
            SELECT pl.id as lesson_id, pl.student_id, s.name as student_name,
                   pl.start_time, pl.teacher
            FROM private_lessons pl
            JOIN students s ON pl.student_id = s.id
            WHERE LOWER(pl.teacher) LIKE ? AND pl.day_of_week = ? AND pl.active = 1
            ORDER BY pl.start_time
        """, (f"%{teacher_query}%", simple_day))
        lessons = cur.fetchall()

    conn.close()

    if not lessons:
        respond(f"Nenhuma aula encontrada para \"{teacher_query}\" em {target_day}")
        return

    teacher_name = lessons[0]['teacher']
    date_str = target_date.isoformat()

    # Check existing attendance
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT student_id, status FROM attendance
        WHERE date = ? AND activity_type = 'aula_individual' AND activity_name = ?
    """, (date_str, teacher_name))
    existing = {row['student_id']: row['status'] for row in cur.fetchall()}
    conn.close()

    # Build checkboxes with time + first name
    options = []
    initial_options = []
    student_ids = []

    for l in lessons:
        time_str = l['start_time'][:5] if l['start_time'] else '?'
        first_name = l['student_name'].split()[0]
        label = f"{time_str} {first_name}"

        option = {
            "text": {"type": "plain_text", "text": label},
            "value": str(l['student_id'])
        }
        options.append(option)
        student_ids.append(l['student_id'])

        if existing.get(l['student_id']) == 'presente' or l['student_id'] not in existing:
            initial_options.append(option)

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"📋 Aulas {teacher_name} - {date_str}"}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Desmarque os alunos que *faltaram*:"}
        },
        {
            "type": "actions",
            "block_id": f"attendance_aula_{teacher_name}_{date_str}",
            "elements": [
                {
                    "type": "checkboxes",
                    "action_id": "attendance_checkboxes",
                    "options": options,
                    "initial_options": initial_options if initial_options else None
                }
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "💾 Salvar"},
                    "style": "primary",
                    "action_id": "save_attendance_aula",
                    "value": json.dumps({
                        "teacher": teacher_name,
                        "date": date_str,
                        "student_ids": student_ids
                    })
                }
            ]
        }
    ]

    if not initial_options:
        blocks[2]["elements"][0].pop("initial_options", None)

    respond(blocks=blocks)


@app.action("save_attendance_aula")
def handle_save_attendance_aula(ack, body, client, logger):
    """Save private lesson attendance to database."""
    ack()

    try:
        action = next(a for a in body["actions"] if a["action_id"] == "save_attendance_aula")
        metadata = json.loads(action["value"])

        checked_ids = set()
        for block in body.get("state", {}).get("values", {}).values():
            if "attendance_checkboxes" in block:
                for option in block["attendance_checkboxes"].get("selected_options", []):
                    checked_ids.add(int(option["value"]))

        conn = get_db()
        cur = conn.cursor()
        user = body["user"]["username"]

        present_count = 0
        absent_count = 0

        for student_id in metadata["student_ids"]:
            status = "presente" if student_id in checked_ids else "falta"
            if status == "presente":
                present_count += 1
            else:
                absent_count += 1

            cur.execute("""
                INSERT INTO attendance (date, activity_type, activity_name, student_id, status, recorded_by)
                VALUES (?, 'aula_individual', ?, ?, ?, ?)
                ON CONFLICT(date, activity_type, activity_name, student_id)
                DO UPDATE SET status = ?, recorded_by = ?, recorded_at = CURRENT_TIMESTAMP
            """, (metadata["date"], metadata["teacher"], student_id, status, user, status, user))

        conn.commit()
        conn.close()

        client.chat_update(
            channel=body["channel"]["id"],
            ts=body["message"]["ts"],
            text=f"✅ Presença salva: Aulas {metadata['teacher']} - {metadata['date']}",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"✅ *Presença salva!*\n\n*Aulas {metadata['teacher']}* - {metadata['date']}\n\n✓ Presentes: {present_count}\n✗ Faltas: {absent_count}\n\n_Registrado por @{user}_"
                    }
                }
            ]
        )

    except Exception as e:
        logger.error(f"Error saving lesson attendance: {e}")
        client.chat_postMessage(
            channel=body["channel"]["id"],
            text=f"❌ Erro ao salvar presença: {str(e)}"
        )


@app.action("attendance_checkboxes")
def handle_attendance_checkboxes(ack, body, logger):
    """Handle checkbox changes - just acknowledge, save happens on button click."""
    ack()


@app.action("save_attendance")
def handle_save_attendance(ack, body, client, logger):
    """Save attendance to database."""
    ack()

    try:
        # Get the button value (metadata)
        action = next(a for a in body["actions"] if a["action_id"] == "save_attendance")
        metadata = json.loads(action["value"])

        # Get checked student IDs from the checkbox state
        checked_ids = set()
        for block in body.get("state", {}).get("values", {}).values():
            if "attendance_checkboxes" in block:
                for option in block["attendance_checkboxes"].get("selected_options", []):
                    checked_ids.add(int(option["value"]))

        # Save to database
        conn = get_db()
        cur = conn.cursor()
        user = body["user"]["username"]

        present_count = 0
        absent_count = 0

        for student_id in metadata["student_ids"]:
            status = "presente" if student_id in checked_ids else "falta"
            if status == "presente":
                present_count += 1
            else:
                absent_count += 1

            cur.execute("""
                INSERT INTO attendance (date, activity_type, activity_name, student_id, status, recorded_by)
                VALUES (?, 'banda', ?, ?, ?, ?)
                ON CONFLICT(date, activity_type, activity_name, student_id)
                DO UPDATE SET status = ?, recorded_by = ?, recorded_at = CURRENT_TIMESTAMP
            """, (metadata["date"], metadata["band"], student_id, status, user, status, user))

        conn.commit()
        conn.close()

        # Update the message to show confirmation
        client.chat_update(
            channel=body["channel"]["id"],
            ts=body["message"]["ts"],
            text=f"✅ Presença salva: {metadata['band']} - {metadata['date']}",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"✅ *Presença salva!*\n\n*{metadata['band']}* - {metadata['date']}\n\n✓ Presentes: {present_count}\n✗ Faltas: {absent_count}\n\n_Registrado por @{user}_"
                    }
                }
            ]
        )

    except Exception as e:
        logger.error(f"Error saving attendance: {e}")
        client.chat_postMessage(
            channel=body["channel"]["id"],
            text=f"❌ Erro ao salvar presença: {str(e)}"
        )


@app.event("message")
def handle_message(event, say):
    """Handle messages - look for ATUALIZAÇÃO: commands."""
    text = event.get("text", "")

    if text.upper().startswith("ATUALIZAÇÃO:") or text.upper().startswith("ATUALIZACAO:"):
        # For now, just acknowledge - full implementation later
        say("Recebi a solicitação de atualização. Implementação em progresso...")


@app.event("app_mention")
def handle_mention(event, say):
    """Handle @mentions."""
    say("Oi! Use os comandos:\n• `/aluno <id ou nome>`\n• `/banda <nome>`\n• `/horario <professor>`")


# Error handler
@app.error
def handle_error(error, body, logger):
    logger.error(f"Error: {error}")
    logger.error(f"Body: {body}")


if __name__ == "__main__":
    print(f"Database: {DB_PATH}")
    print(f"Database exists: {DB_PATH.exists()}")
    print("Starting Favela Brass bot...")
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
