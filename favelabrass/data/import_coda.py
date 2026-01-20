#!/usr/bin/env python3
"""Import Coda CSV exports into SQLite database."""

import csv
import sqlite3
import os
from datetime import datetime

DB_PATH = "/Users/tom/Documents/HQ/favelabrass/data/favelabrass.db"
CSV_DIR = "/Users/tom/Documents/HQ/favelabrass/imports/Coda Program Tables"

def parse_date(date_str):
    """Parse DD/MM/YYYY date format to ISO format."""
    if not date_str or date_str.strip() in ('', '\n'):
        return None
    date_str = date_str.strip()
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None

def parse_bool(val):
    """Parse boolean values."""
    if not val:
        return None
    val = str(val).strip().lower()
    if val in ('true', 'sim', '1', 'yes', '✅'):
        return 1
    if val in ('false', 'não', 'nao', '0', 'no'):
        return 0
    return None

def parse_decimal(val):
    """Parse Brazilian decimal format (comma as decimal separator)."""
    if not val or val.strip() == '':
        return None
    val = str(val).strip()
    # Remove currency symbols and spaces
    val = val.replace('R$', '').replace('$', '').replace(' ', '')
    # Handle Brazilian format: 1.234,56 -> 1234.56
    if ',' in val and '.' in val:
        val = val.replace('.', '').replace(',', '.')
    elif ',' in val:
        val = val.replace(',', '.')
    try:
        return float(val)
    except ValueError:
        return None

def clean_string(val):
    """Clean string values."""
    if val is None:
        return None
    val = str(val).strip()
    if val in ('', '\n', '\r\n'):
        return None
    return val

def read_csv(filename):
    """Read CSV file with proper encoding."""
    filepath = os.path.join(CSV_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def create_tables(conn):
    """Create all tables."""
    c = conn.cursor()

    # Drop existing program tables (keep financial tables)
    tables_to_drop = [
        'students', 'teachers', 'bands', 'instruments', 'instrument_types',
        'band_assignments', 'instrument_loans', 'assessments', 'student_progress',
        'promotions', 'arrangements', 'activities', 'repairs', 'teacher_payments',
        'exit_reasons', 'levels', 'ex_students', 'weeks_per_month'
    ]
    for table in tables_to_drop:
        c.execute(f"DROP TABLE IF EXISTS {table}")

    # Core tables
    c.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birth_date DATE,
            gender TEXT,
            lives_in_community INTEGER,
            community TEXT,
            enrollment_date DATE,
            status TEXT,
            exit_date DATE,
            exit_reason TEXT,
            school TEXT,
            uniform_size TEXT,
            image_authorization INTEGER,
            special_needs TEXT,
            medical_condition TEXT,
            medications TEXT,
            allergies TEXT,
            has_warnings INTEGER,
            suspended_this_semester INTEGER,
            total_warnings INTEGER,
            notes TEXT,
            age INTEGER,
            max_level_tested INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hourly_rate REAL,
            role TEXT,
            status TEXT,
            instruments_taught TEXT
        )
    """)

    c.execute("""
        CREATE TABLE bands (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            is_active INTEGER,
            conductor TEXT,
            period TEXT,
            target_size INTEGER,
            description TEXT
        )
    """)

    c.execute("""
        CREATE TABLE instrument_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sort_order INTEGER,
            family TEXT,
            requires_loan INTEGER,
            min_age INTEGER,
            replacement_value REAL,
            notes TEXT
        )
    """)

    c.execute("""
        CREATE TABLE instruments (
            id INTEGER PRIMARY KEY,
            type TEXT,
            brand_model TEXT,
            is_written_off INTEGER,
            writeoff_reason TEXT,
            patrimony_status TEXT,
            quality TEXT,
            serial_number TEXT,
            has_case INTEGER,
            notes TEXT,
            current_condition TEXT,
            usable INTEGER,
            current_problem TEXT,
            open_repair_cost REAL,
            active_loan_to TEXT,
            loan_category TEXT
        )
    """)

    # Relationship tables
    c.execute("""
        CREATE TABLE band_assignments (
            id TEXT PRIMARY KEY,
            band_id TEXT,
            student_name TEXT,
            next_semester_band TEXT,
            start_date DATE,
            notes TEXT,
            graduation_year INTEGER,
            current_instrument TEXT,
            projected_instrument TEXT
        )
    """)

    c.execute("""
        CREATE TABLE instrument_loans (
            id TEXT PRIMARY KEY,
            instrument_id INTEGER,
            instrument_type TEXT,
            student_name TEXT,
            ex_student_name TEXT,
            teacher_name TEXT,
            person_name TEXT,
            category TEXT,
            loan_date DATE,
            return_date DATE,
            status TEXT,
            notes TEXT,
            registered_by TEXT
        )
    """)

    c.execute("""
        CREATE TABLE assessments (
            id TEXT PRIMARY KEY,
            student_name TEXT,
            category TEXT,
            instrument TEXT,
            score_piece_1 REAL,
            score_piece_2 REAL,
            score_piece_3 REAL,
            score_scales REAL,
            score_sight_reading REAL,
            score_technical REAL,
            score_aural REAL,
            auto_total REAL,
            manual_score REAL,
            final_score REAL,
            result TEXT,
            certificate_issued INTEGER,
            certificate_date DATE,
            examiner TEXT,
            level_tested INTEGER,
            notes TEXT,
            assessment_date DATE,
            assessment_type TEXT
        )
    """)

    c.execute("""
        CREATE TABLE student_progress (
            id TEXT PRIMARY KEY,
            student_name TEXT,
            current_instrument TEXT,
            instrument_2026 TEXT,
            book_level TEXT,
            theory_book TEXT,
            theory_projected_2026 TEXT,
            enrolled_theory_practice TEXT,
            book_projected_2026 TEXT
        )
    """)

    c.execute("""
        CREATE TABLE promotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            instrument TEXT,
            from_band INTEGER,
            to_band INTEGER,
            within_capacity INTEGER,
            level_coherent INTEGER,
            band_coherent INTEGER,
            type TEXT,
            notes TEXT
        )
    """)

    # Operational tables
    c.execute("""
        CREATE TABLE arrangements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            artist TEXT,
            style TEXT,
            has_dorico INTEGER,
            status TEXT,
            difficulty TEXT,
            missing_instruments TEXT,
            notes TEXT,
            score_url TEXT,
            video_score_url TEXT,
            video_performance_url TEXT,
            needs_revision INTEGER,
            video_percussion_url TEXT
        )
    """)

    c.execute("""
        CREATE TABLE activities (
            id TEXT PRIMARY KEY,
            day_of_week TEXT,
            name TEXT,
            type TEXT,
            start_time TEXT,
            end_time TEXT,
            duration_hours REAL,
            location TEXT,
            teacher TEXT
        )
    """)

    c.execute("""
        CREATE TABLE repairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instrument_id INTEGER,
            severity TEXT,
            problem_description TEXT,
            budget REAL,
            status TEXT,
            reported_by TEXT,
            date DATE,
            notes TEXT
        )
    """)

    c.execute("""
        CREATE TABLE teacher_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_name TEXT,
            month TEXT,
            weekly_hours REAL,
            monthly_hours REAL,
            hourly_rate REAL,
            monthly_total REAL
        )
    """)

    # Lookup tables
    c.execute("""
        CREATE TABLE exit_reasons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reason TEXT,
            category TEXT,
            reentry_possible INTEGER,
            notes TEXT
        )
    """)

    c.execute("""
        CREATE TABLE levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

    c.execute("""
        CREATE TABLE ex_students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            id_number TEXT,
            phone TEXT,
            current_profession TEXT,
            instrument_borrowed TEXT,
            cacilda_member INTEGER,
            notes TEXT
        )
    """)

    c.execute("""
        CREATE TABLE weeks_per_month (
            month TEXT PRIMARY KEY,
            mon INTEGER,
            tue INTEGER,
            wed INTEGER,
            thu INTEGER,
            fri INTEGER,
            sat INTEGER
        )
    """)

    conn.commit()

def import_students(conn):
    """Import students from Cadastro_Alunos.csv"""
    rows = read_csv("Cadastro_Alunos.csv")
    c = conn.cursor()

    for row in rows:
        name = clean_string(row.get('Nome do Aluno'))
        if not name:
            continue

        c.execute("""
            INSERT INTO students (
                name, birth_date, gender, lives_in_community, community,
                enrollment_date, status, exit_date, exit_reason, school,
                uniform_size, image_authorization, special_needs, medical_condition,
                medications, allergies, has_warnings, suspended_this_semester,
                total_warnings, notes, age, max_level_tested
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            parse_date(row.get('data_nascimento')),
            clean_string(row.get('genero')),
            parse_bool(row.get('residente_comunidade')),
            clean_string(row.get('qual_comunidade')),
            parse_date(row.get('data_matricula')),
            clean_string(row.get('status')),
            parse_date(row.get('data_saida')),
            clean_string(row.get('motivo_saida')),
            clean_string(row.get('Escola')),
            clean_string(row.get('tamanho_uniforme')),
            parse_bool(row.get('autorizacao_uso_imagem')),
            clean_string(row.get('necessidades_especiais')),
            clean_string(row.get('condição_medica')),
            clean_string(row.get('medicamentos')),
            clean_string(row.get('alergias')),
            parse_bool(row.get('tem_advertências_disciplinares')),
            parse_bool(row.get('suspenso_neste_semestre')),
            clean_string(row.get('total_advertências_neste_semestre')),
            clean_string(row.get('observacoes')),
            clean_string(row.get('Idade')),
            clean_string(row.get('Nivel_Max_Prova'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM students").fetchone()[0]

def import_teachers(conn):
    """Import teachers from Professores.csv"""
    rows = read_csv("Professores [TABELA BASE].csv")
    c = conn.cursor()

    for row in rows:
        name = clean_string(row.get('Professor'))
        if not name:
            continue

        c.execute("""
            INSERT INTO teachers (name, hourly_rate, role, status, instruments_taught)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            parse_decimal(row.get('Valor Hora (R$)')),
            clean_string(row.get('Função')),
            clean_string(row.get('Situação')),
            clean_string(row.get('Instrumentos que lecione'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM teachers").fetchone()[0]

def import_bands(conn):
    """Import bands from Bandas_Grupos.csv"""
    rows = read_csv("Bandas_Grupos [Tabela Base].csv")
    c = conn.cursor()

    for row in rows:
        band_id = clean_string(row.get('banda_id'))
        if not band_id:
            continue

        c.execute("""
            INSERT INTO bands (id, name, is_active, conductor, period, target_size, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            band_id,
            clean_string(row.get('Banda/Grupo')),
            parse_bool(row.get('esta_ativa')),
            clean_string(row.get('Regentes/Professores')),
            clean_string(row.get('periodo')),
            clean_string(row.get('tamanho_previsto')),
            clean_string(row.get('descricao'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM bands").fetchone()[0]

def import_instrument_types(conn):
    """Import instrument types."""
    rows = read_csv("Tipos de Instrumentos.csv")
    c = conn.cursor()

    for row in rows:
        name = clean_string(row.get('Tipo de instrumento'))
        if not name:
            continue

        c.execute("""
            INSERT INTO instrument_types (name, sort_order, family, requires_loan, min_age, replacement_value, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            clean_string(row.get('Score Order')),
            clean_string(row.get('Família')),
            parse_bool(row.get('Requer empréstimo')),
            clean_string(row.get('Idade p/começar')),
            parse_decimal(row.get('Valor de Reposicão')),
            clean_string(row.get('Comentários'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM instrument_types").fetchone()[0]

def import_instruments(conn):
    """Import instruments from Inventário.csv"""
    rows = read_csv("Inventário dos instrumentos [TABELA BASE].csv")
    c = conn.cursor()

    for row in rows:
        inst_id = clean_string(row.get('ID Instrumento (FBx)'))
        if not inst_id:
            continue
        try:
            inst_id = int(inst_id)
        except ValueError:
            continue

        c.execute("""
            INSERT OR REPLACE INTO instruments (
                id, type, brand_model, is_written_off, writeoff_reason,
                patrimony_status, quality, serial_number, has_case, notes,
                current_condition, usable, current_problem, open_repair_cost,
                active_loan_to, loan_category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            inst_id,
            clean_string(row.get('Tipo de Instrumento')),
            clean_string(row.get('Marca/Modelo')),
            parse_bool(row.get('Baixado?')),
            clean_string(row.get('Motivo p/Baixar')),
            clean_string(row.get('Situação Patrimonial (auto)')),
            clean_string(row.get('Qualidade')),
            clean_string(row.get('Número de Série')),
            parse_bool(row.get('Tem Case?')),
            clean_string(row.get('Anotações')),
            clean_string(row.get('Estado atual (auto)')),
            parse_bool(row.get('Pode usar?')),
            clean_string(row.get('Problema atual')),
            parse_decimal(row.get('Custo reparos (aberto)')),
            clean_string(row.get('Empréstimo Ativo')),
            clean_string(row.get('Categoria Empréstimo (auto)'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM instruments").fetchone()[0]

def import_band_assignments(conn):
    """Import band assignments."""
    rows = read_csv("Atribuição Bandas_Grupos [TABELA BASE].csv")
    c = conn.cursor()

    for row in rows:
        assign_id = clean_string(row.get('atribuicao_id'))
        if not assign_id:
            continue

        c.execute("""
            INSERT INTO band_assignments (
                id, band_id, student_name, next_semester_band, start_date,
                notes, graduation_year, current_instrument, projected_instrument
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assign_id,
            clean_string(row.get('Banda Atual')),
            clean_string(row.get('Nome Completo')),
            clean_string(row.get('Atribuição Próximo Semetre')),
            parse_date(row.get('data_inicio')),
            clean_string(row.get('observacoes')),
            clean_string(row.get('ano_final')),
            clean_string(row.get('Instrumento Atual')),
            clean_string(row.get('Instrumento Projetado'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM band_assignments").fetchone()[0]

def import_loans(conn):
    """Import instrument loans."""
    rows = read_csv("Empréstimos.csv")
    c = conn.cursor()

    for row in rows:
        loan_id = clean_string(row.get('ID Emprestimo'))
        if not loan_id:
            continue

        c.execute("""
            INSERT INTO instrument_loans (
                id, instrument_id, instrument_type, student_name, ex_student_name,
                teacher_name, person_name, category, loan_date, return_date,
                status, notes, registered_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            loan_id,
            clean_string(row.get('ID Instrumento')),
            clean_string(row.get('Tipo de Instrumento')),
            clean_string(row.get('Aluno')),
            clean_string(row.get('Ex-Aluno')),
            clean_string(row.get('Professor')),
            clean_string(row.get('Pessoa (auto)')),
            clean_string(row.get('Categoria (auto)')),
            parse_date(row.get('Data Emprestimo')),
            parse_date(row.get('Data Devolução')),
            clean_string(row.get('Status')),
            clean_string(row.get('Obs')),
            clean_string(row.get('Registrado por'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM instrument_loans").fetchone()[0]

def import_assessments(conn):
    """Import assessments."""
    rows = read_csv("Avaliações [TABELA BASE].csv")
    c = conn.cursor()

    for row in rows:
        assess_id = clean_string(row.get('avaliacao_id'))
        if not assess_id:
            continue

        c.execute("""
            INSERT INTO assessments (
                id, student_name, category, instrument, score_piece_1, score_piece_2,
                score_piece_3, score_scales, score_sight_reading, score_technical,
                score_aural, auto_total, manual_score, final_score, result,
                certificate_issued, certificate_date, examiner, level_tested,
                notes, assessment_date, assessment_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assess_id,
            clean_string(row.get('aluno_id')),
            clean_string(row.get('categoria_avaliacao')),
            clean_string(row.get('instrumento')),
            parse_decimal(row.get('pontuacao_peca_1')),
            parse_decimal(row.get('pontuacao_peca_2')),
            parse_decimal(row.get('pontuacao_peca_3')),
            parse_decimal(row.get('pontuacao_escalas_arpejos')),
            parse_decimal(row.get('pontuacao_leitura_vista')),
            parse_decimal(row.get('pontuacao_exercicios_tecnicos')),
            parse_decimal(row.get('pontuacao_percepcao_auditiva')),
            parse_decimal(row.get('pontuacao_total_auto')),
            parse_decimal(row.get('pontuação_manual')),
            parse_decimal(row.get('pontuacao_final')),
            clean_string(row.get('resultado')),
            parse_bool(row.get('certificado_emitido')),
            parse_date(row.get('data_emissao_certificado')),
            clean_string(row.get('avaliador')),
            clean_string(row.get('nivel_testado')),
            clean_string(row.get('observacoes')),
            parse_date(row.get('data_avaliacao')),
            clean_string(row.get('tipo_avaliacao'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM assessments").fetchone()[0]

def import_student_progress(conn):
    """Import student progress."""
    rows = read_csv("Progresso dos Alunos [TABELA BASE].csv")
    c = conn.cursor()

    for row in rows:
        prog_id = clean_string(row.get('progresso_id'))
        if not prog_id:
            continue

        c.execute("""
            INSERT OR REPLACE INTO student_progress (
                id, student_name, current_instrument, instrument_2026,
                book_level, theory_book, theory_projected_2026,
                enrolled_theory_practice, book_projected_2026
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prog_id,
            clean_string(row.get('aluno_nome')),
            clean_string(row.get('instrumento_atual')),
            clean_string(row.get('instrumento_2026')),
            clean_string(row.get('nivel_livro')),
            clean_string(row.get('teoria_livro')),
            clean_string(row.get('teoria_projetado_2026.1')),
            clean_string(row.get('inscrito_teoria_pratica')),
            clean_string(row.get('livro_projetado_2026.1'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM student_progress").fetchone()[0]

def import_promotions(conn):
    """Import promotions/demotions."""
    rows = read_csv("Promoções_Rebaixamentos.csv")
    c = conn.cursor()

    for row in rows:
        name = clean_string(row.get('Name'))
        if not name:
            continue

        c.execute("""
            INSERT INTO promotions (
                student_name, instrument, from_band, to_band,
                within_capacity, level_coherent, band_coherent, type, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            clean_string(row.get('Instrumento')),
            clean_string(row.get('De Banda')),
            clean_string(row.get('Para Banda')),
            parse_bool(row.get('Dentro de Capacidade?')),
            parse_bool(row.get('Coerência Nível?')),
            parse_bool(row.get('Coerência Banda?')),
            clean_string(row.get('Regular/Exeção')),
            clean_string(row.get('Notes'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM promotions").fetchone()[0]

def import_arrangements(conn):
    """Import arrangements."""
    rows = read_csv("Arranjos [TABELA BASE].csv")
    c = conn.cursor()

    for row in rows:
        title = clean_string(row.get('Tîtulo'))
        if not title:
            continue

        c.execute("""
            INSERT INTO arrangements (
                title, artist, style, has_dorico, status, difficulty,
                missing_instruments, notes, score_url, video_score_url,
                video_performance_url, needs_revision, video_percussion_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title,
            clean_string(row.get('Artista')),
            clean_string(row.get('Estilo')),
            parse_bool(row.get('Arquivo Dorico')),
            clean_string(row.get('Status')),
            clean_string(row.get('Dificuldade')),
            clean_string(row.get('Instrumentos Faltando')),
            clean_string(row.get('Obs')),
            clean_string(row.get('Partitura')),
            clean_string(row.get('Vídeo Partitura')),
            clean_string(row.get('Vídeo Performance')),
            parse_bool(row.get('Precisa Revisão')),
            clean_string(row.get('Vídeo Perc'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM arrangements").fetchone()[0]

def import_activities(conn):
    """Import activities/schedule."""
    rows = read_csv("Atividades_Roteiro [TABELA BASE].csv")
    c = conn.cursor()

    for row in rows:
        act_id = clean_string(row.get('atividade_id'))
        if not act_id:
            continue

        c.execute("""
            INSERT INTO activities (
                id, day_of_week, name, type, start_time, end_time,
                duration_hours, location, teacher
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            act_id,
            clean_string(row.get('dia_semana')),
            clean_string(row.get('nome')),
            clean_string(row.get('tipo')),
            clean_string(row.get('horario_inicio')),
            clean_string(row.get('horario_fim')),
            parse_decimal(row.get('duração_horas')),
            clean_string(row.get('local')),
            clean_string(row.get('professor_responsavel'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM activities").fetchone()[0]

def import_repairs(conn):
    """Import repairs."""
    rows = read_csv("Reparos [TABELA BASE].csv")
    c = conn.cursor()

    for row in rows:
        inst_id = clean_string(row.get('ID Instrumento (FBx)'))
        if not inst_id:
            continue

        c.execute("""
            INSERT INTO repairs (
                instrument_id, severity, problem_description, budget,
                status, reported_by, date, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            inst_id,
            clean_string(row.get('Severidade')),
            clean_string(row.get('Descrição Problema')),
            parse_decimal(row.get('Orçamento')),
            clean_string(row.get('Status')),
            clean_string(row.get('Reportado por')),
            parse_date(row.get('Data')),
            clean_string(row.get('Notas/Anexos'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM repairs").fetchone()[0]

def import_teacher_payments(conn):
    """Import teacher payment calculations."""
    rows = read_csv("Cálculo Mensal.csv")
    c = conn.cursor()

    for row in rows:
        teacher = clean_string(row.get('Professor'))
        if not teacher:
            continue

        c.execute("""
            INSERT INTO teacher_payments (
                teacher_name, month, weekly_hours, monthly_hours,
                hourly_rate, monthly_total
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            teacher,
            clean_string(row.get('Mês')),
            parse_decimal(row.get('Horas semanais')),
            parse_decimal(row.get('Horas no mês')),
            parse_decimal(row.get('Valor Hora (R$)')),
            parse_decimal(row.get('Valor Total Mês'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM teacher_payments").fetchone()[0]

def import_exit_reasons(conn):
    """Import exit reasons lookup."""
    rows = read_csv("Motivo de Saída.csv")
    c = conn.cursor()

    for row in rows:
        reason = clean_string(row.get('Motivo'))
        if not reason:
            continue

        c.execute("""
            INSERT INTO exit_reasons (reason, category, reentry_possible, notes)
            VALUES (?, ?, ?, ?)
        """, (
            reason,
            clean_string(row.get('Categoria')),
            parse_bool(row.get('Re-ingresso possível?')),
            clean_string(row.get('Obs'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM exit_reasons").fetchone()[0]

def import_levels(conn):
    """Import levels lookup."""
    rows = read_csv("Níveis.csv")
    c = conn.cursor()

    for row in rows:
        name = clean_string(row.get('Nível'))
        if not name:
            continue
        c.execute("INSERT INTO levels (name) VALUES (?)", (name,))

    # Also add books from Livros.csv
    rows = read_csv("Livros.csv")
    for row in rows:
        name = clean_string(row.get('Name'))
        if not name:
            continue
        c.execute("INSERT INTO levels (name) VALUES (?)", (name,))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM levels").fetchone()[0]

def import_ex_students(conn):
    """Import ex-students/alumni."""
    rows = read_csv("Ex-alunos.csv")
    c = conn.cursor()

    for row in rows:
        name = clean_string(row.get('Nome Completo'))
        if not name:
            continue

        c.execute("""
            INSERT INTO ex_students (
                name, id_number, phone, current_profession,
                instrument_borrowed, cacilda_member, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            clean_string(row.get('Identidade')),
            clean_string(row.get('No. Celular')),
            clean_string(row.get('Profissão Atual')),
            clean_string(row.get('Instrumento Emprestado')),
            parse_bool(row.get('Integrante da Cacilda?')),
            clean_string(row.get('Obs'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM ex_students").fetchone()[0]

def import_weeks_per_month(conn):
    """Import weeks per month config."""
    rows = read_csv("Semanas por mês 2026.csv")
    c = conn.cursor()

    for row in rows:
        month = clean_string(row.get('Mês'))
        if not month:
            continue

        c.execute("""
            INSERT INTO weeks_per_month (month, mon, tue, wed, thu, fri, sat)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            month,
            clean_string(row.get('Seg')),
            clean_string(row.get('Ter')),
            clean_string(row.get('Qua')),
            clean_string(row.get('Qui')),
            clean_string(row.get('Sex')),
            clean_string(row.get('Sáb'))
        ))

    conn.commit()
    return c.execute("SELECT COUNT(*) FROM weeks_per_month").fetchone()[0]

def main():
    conn = sqlite3.connect(DB_PATH)

    print("Creating tables...")
    create_tables(conn)

    print("\nImporting data...")
    results = {}

    # Core tables
    results['students'] = import_students(conn)
    results['teachers'] = import_teachers(conn)
    results['bands'] = import_bands(conn)
    results['instrument_types'] = import_instrument_types(conn)
    results['instruments'] = import_instruments(conn)

    # Relationship tables
    results['band_assignments'] = import_band_assignments(conn)
    results['instrument_loans'] = import_loans(conn)
    results['assessments'] = import_assessments(conn)
    results['student_progress'] = import_student_progress(conn)
    results['promotions'] = import_promotions(conn)

    # Operational tables
    results['arrangements'] = import_arrangements(conn)
    results['activities'] = import_activities(conn)
    results['repairs'] = import_repairs(conn)
    results['teacher_payments'] = import_teacher_payments(conn)

    # Lookup tables
    results['exit_reasons'] = import_exit_reasons(conn)
    results['levels'] = import_levels(conn)
    results['ex_students'] = import_ex_students(conn)
    results['weeks_per_month'] = import_weeks_per_month(conn)

    print("\n" + "="*50)
    print("IMPORT RESULTS")
    print("="*50)
    for table, count in results.items():
        print(f"{table:25} {count:>6} rows")
    print("="*50)
    print(f"{'TOTAL':25} {sum(results.values()):>6} rows")

    conn.close()

if __name__ == "__main__":
    main()
