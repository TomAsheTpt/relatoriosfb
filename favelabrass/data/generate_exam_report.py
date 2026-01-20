#!/usr/bin/env python3
"""
Generate branded PDF exam reports from the assessments_practical table.

Usage:
    python3 generate_exam_report.py <assessment_id>
    python3 generate_exam_report.py AV-204

Output goes to favelabrass/outputs/relatorio_prova_<student_name>.pdf
"""

import sys
import sqlite3
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.platypus import Flowable

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, 'favelabrass.db')
LOGO_PATH = os.path.join(SCRIPT_DIR, '..', 'assets', 'Logo FB White.png')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', 'outputs')

# Brand colors
PURPLE = colors.HexColor('#5A0E7A')
DARK_PURPLE = colors.HexColor('#3E0B59')
YELLOW = colors.HexColor('#FEF100')
GREEN = colors.HexColor('#62CC3C')


class LogoWithBackground(Flowable):
    """Logo on a colored rounded rectangle background."""
    def __init__(self, logo_path, width, height, bg_color):
        Flowable.__init__(self)
        self.logo_path = logo_path
        self.width = width
        self.height = height
        self.bg_color = bg_color

    def draw(self):
        self.canv.setFillColor(self.bg_color)
        self.canv.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        logo_width = self.width * 0.85
        logo_height = self.height * 0.7
        x = (self.width - logo_width) / 2
        y = (self.height - logo_height) / 2
        self.canv.drawImage(self.logo_path, x, y, logo_width, logo_height,
                           preserveAspectRatio=True, mask='auto')


def get_result_label(score):
    """Return Portuguese result label based on MTB grade bands."""
    if score >= 87:
        return "Distinção"
    elif score >= 75:
        return "Mérito"
    elif score >= 60:
        return "Aprovado"
    elif score >= 45:
        return "Azul"
    else:
        return "Branco"


def generate_report(assessment_id):
    """Generate PDF report for a given assessment ID."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Fetch assessment data with full breakdown
    c.execute("""
        SELECT
            a.id, a.student_id, a.student_name, a.assessment_date, a.instrument,
            a.level_tested, a.total_score, a.result, a.examiner, a.notes,
            a.score_piece_1, a.score_piece_2, a.score_piece_3,
            a.score_scales, a.score_sight_reading,
            a.examiner_comments_pt,
            a.piece1_name, a.piece1_accuracy, a.piece1_expression, a.piece1_technique,
            a.piece2_name, a.piece2_accuracy, a.piece2_expression, a.piece2_technique,
            a.piece3_name, a.piece3_accuracy, a.piece3_expression, a.piece3_technique,
            a.score_scales_only, a.score_technical_exercises, a.score_listening
        FROM assessments_practical a
        WHERE a.id = ?
    """, (assessment_id,))

    row = c.fetchone()
    if not row:
        print(f"Error: Assessment {assessment_id} not found")
        sys.exit(1)

    (assess_id, student_id, student_name, assess_date, instrument,
     level, score, result, examiner, notes,
     piece1_score, piece2_score, piece3_score,
     scales_score, reading_score,
     comments_pt,
     piece1_name, piece1_acc, piece1_exp, piece1_tech,
     piece2_name, piece2_acc, piece2_exp, piece2_tech,
     piece3_name, piece3_acc, piece3_exp, piece3_tech,
     scales_only, tech_exercises, listening_score) = row

    conn.close()

    # Parse scores (format: "15/20" or just numbers)
    def parse_score(s):
        if s is None:
            return None, None
        if '/' in str(s):
            parts = str(s).split('/')
            return int(parts[0]), int(parts[1])
        return int(s), None

    # Calculate result label
    result_label = get_result_label(score) if score else result

    # Output path
    safe_name = student_name.lower().replace(' ', '_')
    output_path = os.path.join(OUTPUT_DIR, f'relatorio_prova_{safe_name}.pdf')

    # Create PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Comment', fontSize=9, fontName='Helvetica',
                              textColor=colors.black, alignment=TA_LEFT, leading=12))

    elements = []

    # Header with logo
    logo_with_bg = LogoWithBackground(LOGO_PATH, 55*mm, 28*mm, PURPLE)

    info_data = [
        ['Referência:', assess_id],
        ['Candidato:', student_name],
        ['Instrumento:', instrument or 'Trompete'],
        ['Nível:', f'Nível {level}' if level else ''],
        ['Professor:', 'Joe Epstein'],  # TODO: get from DB
        ['Examinador:', examiner or ''],
    ]

    info_table = Table(info_data, colWidths=[25*mm, 55*mm])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))

    header_table = Table([[logo_with_bg, '', info_table]], colWidths=[58*mm, 27*mm, 85*mm])
    header_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(header_table)
    elements.append(Spacer(1, 6*mm))

    # Recital Section
    recital_header = Table([['Seção de Recital', 'Pontuação']], colWidths=[145*mm, 25*mm])
    recital_header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PURPLE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (0, 0), 5),
        ('RIGHTPADDING', (1, 0), (1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
    ]))
    elements.append(recital_header)

    # Pieces with full breakdown
    pieces_info = [
        (piece1_name, piece1_score, piece1_acc, piece1_exp, piece1_tech),
        (piece2_name, piece2_score, piece2_acc, piece2_exp, piece2_tech),
        (piece3_name, piece3_score, piece3_acc, piece3_exp, piece3_tech),
    ]

    pieces_data = []
    for i, (name, total, acc, exp, tech) in enumerate(pieces_info, 1):
        if name or total:
            piece_name = name or f'Peça {i}'
            pieces_data.append([f'Peça {i}: {piece_name}', ''])
            # Show breakdown if available, otherwise just total
            if acc is not None and exp is not None and tech is not None:
                breakdown = f'Precisão {acc}/6    Expressão {exp}/7    Técnica {tech}/7'
                total_val = int(total) if total else (acc + exp + tech)
                pieces_data.append([breakdown, f'{total_val}/20'])
            elif total:
                pieces_data.append(['', f'{int(total)}/20'])

    if pieces_data:
        pieces_table = Table(pieces_data, colWidths=[145*mm, 25*mm])
        piece_style = [
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (0, -1), 5),
            ('RIGHTPADDING', (1, 0), (1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
        ]
        # Bold piece names (even rows starting from 0)
        for i in range(0, len(pieces_data), 2):
            piece_style.append(('FONTNAME', (0, i), (0, i), 'Helvetica-Bold'))
            if i + 1 < len(pieces_data):
                piece_style.append(('FONTNAME', (1, i+1), (1, i+1), 'Helvetica-Bold'))
                piece_style.append(('LINEBELOW', (0, i+1), (-1, i+1), 0.5, colors.lightgrey))
        pieces_table.setStyle(TableStyle(piece_style))
        elements.append(pieces_table)

    elements.append(Spacer(1, 5*mm))

    # Technical Section
    if scales_score or scales_only or tech_exercises:
        tech_header = Table([['Seção Técnica', 'Pontuação']], colWidths=[145*mm, 25*mm])
        tech_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PURPLE),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (0, 0), 5),
            ('RIGHTPADDING', (1, 0), (1, 0), 5),
            ('TOPPADDING', (0, 0), (-1, 0), 4),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ]))
        elements.append(tech_header)

        # Use breakdown if available, otherwise combined score
        if scales_only is not None and tech_exercises is not None:
            total_tech = scales_only + tech_exercises
            breakdown = f'Escalas {scales_only}/13    Exercícios Técnicos {tech_exercises}/12'
        else:
            total_tech = int(scales_score) if scales_score else 0
            breakdown = ''

        tech_data = [
            ['Escalas e Exercícios Técnicos', ''],
            [breakdown, f'{total_tech}/25'],
        ]
        tech_table = Table(tech_data, colWidths=[145*mm, 25*mm])
        tech_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, 1), 'Helvetica'),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (0, -1), 5),
            ('RIGHTPADDING', (1, 0), (1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LINEBELOW', (0, 1), (-1, 1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(tech_table)

    # Musicianship Section
    if reading_score or listening_score:
        music_header = Table([['Seção de Musicalidade', 'Pontuação']], colWidths=[145*mm, 25*mm])
        music_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PURPLE),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (0, 0), 5),
            ('RIGHTPADDING', (1, 0), (1, 0), 5),
            ('TOPPADDING', (0, 0), (-1, 0), 4),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ]))
        elements.append(music_header)

        read_val = int(reading_score) if reading_score else 0
        listen_val = int(listening_score) if listening_score else 0
        total_music = read_val + listen_val

        music_data = [
            ['Leitura e Percepção Auditiva', ''],
            [f'Leitura {read_val}/7    Percepção Auditiva {listen_val}/8', f'{total_music}/15'],
        ]
        music_table = Table(music_data, colWidths=[145*mm, 25*mm])
        music_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, 1), 'Helvetica'),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (0, -1), 5),
            ('RIGHTPADDING', (1, 0), (1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LINEBELOW', (0, 1), (-1, 1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(music_table)

    elements.append(Spacer(1, 5*mm))

    # General Comments section - kept together to avoid page break
    general_section = []

    gen_header = Table([['Comentários Gerais']], colWidths=[170*mm])
    gen_header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PURPLE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('LEFTPADDING', (0, 0), (0, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
    ]))
    general_section.append(gen_header)

    # Result box with general comment
    general_comment = comments_pt.split('\n\n')[-1] if comments_pt and '\n\n' in comments_pt else \
                      f"Parabéns por alcançar {result_label.lower()}, {student_name.split()[0]}."

    result_data = [
        [Paragraph(general_comment, styles['Comment']),
         Paragraph(f'<b>{result_label}</b>', ParagraphStyle(name='BigResult', fontSize=24,
                   fontName='Helvetica-Bold', textColor=PURPLE, alignment=TA_CENTER))],
        ['', Paragraph('Distinção (87-100)<br/>Mérito (75-86)<br/>Aprovado (60-74)<br/>Azul (45-59)<br/>Branco (Abaixo de 45)',
                       ParagraphStyle(name='GradeBands', fontSize=8, fontName='Helvetica', alignment=TA_LEFT, leading=10))],
    ]

    result_table = Table(result_data, colWidths=[115*mm, 55*mm])
    result_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (0, 0), (0, 1)),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LINEAFTER', (0, 0), (0, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    general_section.append(result_table)
    general_section.append(Spacer(1, 8*mm))

    # Final mark
    final_data = [[f'Nota Final: {int(score)}/100']]
    final_table = Table(final_data, colWidths=[170*mm])
    final_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 12),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('RIGHTPADDING', (0, 0), (0, 0), 8),
        ('TOPPADDING', (0, 0), (0, 0), 6),
        ('BOTTOMPADDING', (0, 0), (0, 0), 6),
    ]))
    general_section.append(final_table)

    # Wrap general section in KeepTogether to prevent page break
    elements.append(KeepTogether(general_section))

    doc.build(elements)
    print(f"Generated: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 generate_exam_report.py <assessment_id>")
        print("Example: python3 generate_exam_report.py AV-204")
        sys.exit(1)

    assessment_id = sys.argv[1]
    output = generate_report(assessment_id)

    # Open the PDF
    import subprocess
    subprocess.run(['open', output])
