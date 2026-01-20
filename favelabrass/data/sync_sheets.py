#!/usr/bin/env python3
"""
Sync Google Sheets to SQLite database.

Setup:
1. Create a Google Cloud project
2. Enable Google Sheets API
3. Create a service account and download JSON credentials
4. Save credentials to ~/.config/favelabrass/google-credentials.json
5. Share each Sheet with the service account email (view access)

Usage:
    python3 sync_sheets.py                 # Sync all sheets
    python3 sync_sheets.py --sheet alunos  # Sync specific sheet
    python3 sync_sheets.py --dry-run       # Preview without writing
"""

import sqlite3
import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip3 install google-auth google-api-python-client")
    sys.exit(1)

# Configuration
DB_PATH = Path("/Users/tom/Documents/HQ/favelabrass/data/favelabrass.db")
CREDENTIALS_PATH = Path.home() / ".config/favelabrass/google-credentials.json"
SPREADSHEET_ID = None  # Set this after creating the spreadsheet

# Sheet name -> (table name, ID column, column mapping)
# Column mapping: sheet_column -> db_column
SHEET_CONFIG = {
    "Alunos": {
        "table": "students",
        "id_column": "id",
        "columns": {
            "id": "id",
            "nome": "name",
            "data_nascimento": ("birth_date", "date"),
            "genero": "gender",
            "comunidade": "community",
            "mora_em_comunidade": ("lives_in_community", "bool"),
            "escola": "school",
            "data_matricula": ("enrollment_date", "date"),
            "status": "status",
            "data_saida": ("exit_date", "date"),
            "motivo_saida": "exit_reason",
            "tamanho_uniforme": "uniform_size",
            "autorizacao_imagem": ("image_authorization", "bool"),
            "necessidades_especiais": "special_needs",
            "condicao_medica": "medical_condition",
            "observacoes": "notes",
        }
    },
    "Instrumentos": {
        "table": "instruments",
        "id_column": "id",
        "columns": {
            "id": ("id", "int"),
            "tipo": "type",
            "marca_modelo": "brand_model",
            "numero_serie": "serial_number",
            "qualidade": "quality",
            "tem_case": ("has_case", "bool"),
            "baixado": ("is_written_off", "bool"),
            "motivo_baixa": "writeoff_reason",
            "anotacoes": "notes",
        }
    },
    "Emprestimos": {
        "table": "instrument_loans",
        "id_column": "id",
        "columns": {
            "id": "id",
            "instrumento_id": ("instrument_id", "int"),
            "aluno_nome": "student_name",
            "categoria": "category",
            "data_emprestimo": ("loan_date", "date"),
            "data_devolucao": ("return_date", "date"),
            "status": "status",
            "obs": "notes",
        }
    },
    "Avaliacoes": {
        "table": "assessments",
        "id_column": "id",
        "columns": {
            "id": "id",
            "aluno_nome": "student_name",
            "data": ("assessment_date", "date"),
            "tipo": "assessment_type",
            "categoria": "category",
            "nivel_testado": ("level_tested", "int"),
            "instrumento": "instrument",
            "pontuacao_peca_1": ("score_piece_1", "float"),
            "pontuacao_peca_2": ("score_piece_2", "float"),
            "pontuacao_peca_3": ("score_piece_3", "float"),
            "pontuacao_escalas": ("score_scales", "float"),
            "pontuacao_leitura": ("score_sight_reading", "float"),
            "pontuacao_tecnica": ("score_technical", "float"),
            "pontuacao_teoria": ("manual_score", "float"),
            "pontuacao_final": ("final_score", "float"),
            "resultado": "result",
            "avaliador": "examiner",
            "observacoes": "notes",
        }
    },
    "Bandas": {
        "table": "bands",
        "id_column": "id",
        "columns": {
            "id": "id",
            "nome": "name",
            "regente": "conductor",
            "ativa": ("is_active", "bool"),
            "tamanho_previsto": ("target_size", "int"),
            "descricao": "description",
        }
    },
    "Atribuicao_Bandas": {
        "table": "band_assignments",
        "id_column": "id",
        "columns": {
            "id": "id",
            "aluno_nome": "student_name",
            "banda_atual": "band_id",
            "instrumento": "current_instrument",
            "data_inicio": ("start_date", "date"),
            "banda_proxima": "next_semester_band",
            "ano_formatura": ("graduation_year", "int"),
        }
    },
    "Professores": {
        "table": "teachers",
        "id_column": "nome",  # Use name as ID for teachers
        "columns": {
            "nome": "name",
            "funcao": "role",
            "situacao": "status",
            "valor_hora": ("hourly_rate", "float"),
            "instrumentos": "instruments_taught",
        }
    },
    "Atividades": {
        "table": "activities",
        "id_column": "id",
        "columns": {
            "id": "id",
            "dia_semana": "day_of_week",
            "nome": "name",
            "tipo": "type",
            "horario_inicio": "start_time",
            "horario_fim": "end_time",
            "local": "location",
            "professor": "teacher",
        }
    },
}


def parse_date(date_str):
    """Parse DD/MM/YYYY to YYYY-MM-DD."""
    if not date_str or not date_str.strip():
        return None
    date_str = date_str.strip()
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return None


def parse_bool(val):
    """Parse boolean values."""
    if not val:
        return None
    val = str(val).strip().lower()
    if val in ('sim', 'yes', 'true', '1', 's'):
        return 1
    if val in ('não', 'nao', 'no', 'false', '0', 'n'):
        return 0
    return None


def parse_float(val):
    """Parse float, handling Brazilian format."""
    if not val or not str(val).strip():
        return None
    val = str(val).strip().replace(',', '.')
    try:
        return float(val)
    except ValueError:
        return None


def parse_int(val):
    """Parse integer."""
    if not val or not str(val).strip():
        return None
    try:
        return int(float(str(val).strip()))
    except ValueError:
        return None


def parse_value(val, col_spec):
    """Parse a value according to its column specification."""
    if isinstance(col_spec, tuple):
        db_col, col_type = col_spec
        if col_type == "date":
            return db_col, parse_date(val)
        elif col_type == "bool":
            return db_col, parse_bool(val)
        elif col_type == "float":
            return db_col, parse_float(val)
        elif col_type == "int":
            return db_col, parse_int(val)
        else:
            return db_col, val.strip() if val else None
    else:
        return col_spec, val.strip() if val else None


def get_sheets_service():
    """Create Google Sheets API service."""
    if not CREDENTIALS_PATH.exists():
        print(f"Credentials file not found: {CREDENTIALS_PATH}")
        print("\nSetup instructions:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project or select existing")
        print("3. Enable 'Google Sheets API'")
        print("4. Create a Service Account (APIs & Services > Credentials)")
        print("5. Download JSON key file")
        print(f"6. Save to: {CREDENTIALS_PATH}")
        print("7. Share your Google Sheet with the service account email")
        sys.exit(1)

    creds = Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    return build('sheets', 'v4', credentials=creds)


def fetch_sheet_data(service, sheet_name):
    """Fetch all data from a sheet."""
    if not SPREADSHEET_ID:
        print("ERROR: SPREADSHEET_ID not set in sync_sheets.py")
        print("Create your Google Sheet, then add the ID from the URL:")
        print("https://docs.google.com/spreadsheets/d/[THIS-IS-THE-ID]/edit")
        sys.exit(1)

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_name}!A:Z"
    ).execute()

    rows = result.get('values', [])
    if not rows:
        return []

    headers = rows[0]
    data = []
    for row in rows[1:]:
        # Pad row to match headers length
        row = row + [''] * (len(headers) - len(row))
        data.append(dict(zip(headers, row)))

    return data


def sync_sheet(conn, sheet_name, config, rows, dry_run=False):
    """Sync a sheet's data to the database."""
    table = config["table"]
    id_col = config["id_column"]
    columns = config["columns"]

    c = conn.cursor()

    # Get existing IDs
    db_id_col = columns[id_col] if isinstance(columns[id_col], str) else columns[id_col][0]
    c.execute(f"SELECT {db_id_col} FROM {table}")
    existing_ids = set(row[0] for row in c.fetchall())

    inserted = 0
    updated = 0

    for row in rows:
        # Parse all columns
        parsed = {}
        row_id = None

        for sheet_col, col_spec in columns.items():
            val = row.get(sheet_col, '')
            db_col, parsed_val = parse_value(val, col_spec)
            parsed[db_col] = parsed_val

            if sheet_col == id_col:
                row_id = parsed_val

        if not row_id:
            continue  # Skip rows without ID

        # Build upsert query
        db_columns = list(parsed.keys())
        placeholders = ', '.join(['?' for _ in db_columns])
        columns_str = ', '.join(db_columns)

        if row_id in existing_ids:
            # Update
            set_clause = ', '.join([f"{col} = ?" for col in db_columns])
            sql = f"UPDATE {table} SET {set_clause} WHERE {db_id_col} = ?"
            params = list(parsed.values()) + [row_id]
            updated += 1
        else:
            # Insert
            sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
            params = list(parsed.values())
            inserted += 1

        if not dry_run:
            c.execute(sql, params)

    if not dry_run:
        conn.commit()

    return inserted, updated


def main():
    parser = argparse.ArgumentParser(description='Sync Google Sheets to SQLite')
    parser.add_argument('--sheet', help='Sync specific sheet only')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    parser.add_argument('--list', action='store_true', help='List configured sheets')
    args = parser.parse_args()

    if args.list:
        print("Configured sheets:")
        for sheet_name, config in SHEET_CONFIG.items():
            print(f"  {sheet_name} -> {config['table']}")
        return

    print("Connecting to Google Sheets API...")
    service = get_sheets_service()

    print(f"Opening database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)

    sheets_to_sync = [args.sheet] if args.sheet else SHEET_CONFIG.keys()

    print(f"\n{'DRY RUN - no changes will be made' if args.dry_run else 'Syncing...'}\n")

    total_inserted = 0
    total_updated = 0

    for sheet_name in sheets_to_sync:
        if sheet_name not in SHEET_CONFIG:
            print(f"Unknown sheet: {sheet_name}")
            continue

        config = SHEET_CONFIG[sheet_name]
        print(f"Fetching {sheet_name}...", end=" ")

        try:
            rows = fetch_sheet_data(service, sheet_name)
            print(f"got {len(rows)} rows...", end=" ")

            inserted, updated = sync_sheet(conn, sheet_name, config, rows, args.dry_run)
            print(f"inserted {inserted}, updated {updated}")

            total_inserted += inserted
            total_updated += updated

        except Exception as e:
            print(f"ERROR: {e}")

    conn.close()

    print(f"\n{'Would sync' if args.dry_run else 'Synced'}: {total_inserted} new, {total_updated} updated")


if __name__ == "__main__":
    main()
