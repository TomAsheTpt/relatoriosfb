# Enrollment Forms - Favela Brass

## Overview

Two Google Forms for different enrollment paths:

1. **Programa Avançado** - Full enrollment for bands/external lessons
2. **Oficinas nas Escolas** - Simple sign-up for school workshops

Both forms feed into Google Sheets, which sync to SQLite.

---

## Form 1: Matrícula Programa Avançado

**URL:** [Create in Google Forms]
**Response Sheet:** "Novas Matrículas Avançado"

### Form Structure:

**Page 1: Dados do Aluno**

| Question | Type | Required | Validation |
|----------|------|----------|------------|
| Nome completo do aluno | Short text | Yes | |
| Data de nascimento | Date | Yes | |
| Gênero | Multiple choice | Yes | Masculino / Feminino |
| CPF do aluno (se tiver) | Short text | No | Format: XXX.XXX.XXX-XX |

**Page 2: Endereço e Comunidade**

| Question | Type | Required | Notes |
|----------|------|----------|-------|
| Mora em comunidade? | Multiple choice | Yes | Sim / Não |
| Qual comunidade? | Short text | If yes | |
| Bairro | Short text | Yes | |
| Endereço completo | Long text | No | |

**Page 3: Escola**

| Question | Type | Required | Notes |
|----------|------|----------|-------|
| Nome da escola | Short text | Yes | |
| Série/Ano | Dropdown | Yes | 1º ao 9º ano / Ensino Médio / Não estuda |
| Turno | Multiple choice | Yes | Manhã / Tarde / Noite |

**Page 4: Responsável**

| Question | Type | Required | Notes |
|----------|------|----------|-------|
| Nome do responsável | Short text | Yes | |
| Parentesco | Dropdown | Yes | Mãe / Pai / Avó / Avô / Tio(a) / Outro |
| WhatsApp do responsável | Short text | Yes | Format: (XX) XXXXX-XXXX |
| Email do responsável | Short text | No | |

**Page 5: Saúde e Autorizações**

| Question | Type | Required | Notes |
|----------|------|----------|-------|
| O aluno tem alguma necessidade especial? | Long text | No | |
| O aluno tem alguma condição médica? | Long text | No | Asma, epilepsia, etc. |
| O aluno toma algum medicamento regularmente? | Long text | No | |
| O aluno tem alguma alergia? | Long text | No | |
| Autoriza uso de imagem? | Multiple choice | Yes | Sim / Não |
| Tamanho de camiseta | Dropdown | Yes | PP / P / M / G / GG / XGG |

**Page 6: Experiência Musical (opcional)**

| Question | Type | Required | Notes |
|----------|------|----------|-------|
| Já estudou música antes? | Multiple choice | No | Sim / Não |
| Qual instrumento tem interesse? | Checkboxes | No | Trompete / Trombone / Saxofone / Percussão / Não sei ainda |
| Como conheceu o Favela Brass? | Multiple choice | No | Indicação / Redes sociais / Escola / Evento / Outro |

**Confirmation Message:**
```
Obrigado pela inscrição!

Entraremos em contato pelo WhatsApp informado para confirmar a matrícula
e agendar o início das atividades.

Em caso de dúvidas, entre em contato: [WhatsApp do FB]
```

---

## Form 2: Inscrição Oficinas nas Escolas

**URL:** [Create in Google Forms]
**Response Sheet:** "Inscrições Oficinas Escolas"

### Form Structure:

**Single Page - Keep it simple**

| Question | Type | Required | Validation |
|----------|------|----------|------------|
| Nome completo do aluno | Short text | Yes | |
| Data de nascimento | Date | Yes | |
| Escola | Dropdown | Yes | E.M. Pereira Passos / E.M. Estados Unidos / E.M. Mem de Sá / E.M. Vital Brasil / E.M. Maria Leopoldina |
| Série/Ano | Dropdown | Yes | 1º ao 9º ano |
| Turno que estuda | Multiple choice | Yes | Manhã / Tarde |
| Nome do responsável | Short text | Yes | |
| WhatsApp do responsável | Short text | Yes | (XX) XXXXX-XXXX |
| Já participou do Favela Brass antes? | Multiple choice | Yes | Sim / Não / Não sei |

**Confirmation Message:**
```
Inscrição recebida!

As oficinas acontecem no horário do almoço na sua escola.
O professor confirmará a participação na primeira aula.
```

---

## Response Sheets Setup

### Sheet: "Novas Matrículas Avançado"

Add these columns (manually, after form responses):

| Column | Purpose |
|--------|---------|
| status_processamento | Pendente / Processado / Duplicado |
| aluno_id_existente | If matched to existing student |
| aluno_id_novo | New ID if created |
| processado_por | Who processed it |
| data_processamento | When processed |
| notas | Any notes |

### Sheet: "Inscrições Oficinas Escolas"

Add these columns:

| Column | Purpose |
|--------|---------|
| match_status | Novo / Retornando / Verificar |
| aluno_id | Matched or new ID |
| processado | Sim / Não |

---

## Matching Script

Add to sync_sheets.py or create separate script:

```python
def find_matching_student(conn, nome, data_nascimento):
    """
    Find existing student by name + DOB.
    Returns (student_id, confidence) or (None, None)
    """
    c = conn.cursor()

    # Exact match on name + DOB
    c.execute("""
        SELECT id, name, birth_date
        FROM students
        WHERE LOWER(name) = LOWER(?) AND birth_date = ?
    """, (nome.strip(), data_nascimento))

    exact = c.fetchone()
    if exact:
        return exact[0], "exact"

    # Fuzzy match on name only (for Iris to verify)
    c.execute("""
        SELECT id, name, birth_date
        FROM students
        WHERE LOWER(name) LIKE LOWER(?)
    """, (f"%{nome.strip()}%",))

    fuzzy = c.fetchall()
    if fuzzy:
        return fuzzy, "fuzzy"

    return None, None
```

---

## Iris Workflow

### Daily/Weekly during enrollment period:

**For Advanced Program submissions:**

1. Open "Novas Matrículas Avançado" sheet
2. Filter: `status_processamento = Pendente`
3. For each row:
   - Check if name + DOB matches existing student
   - If match: mark as Duplicado, note existing ID
   - If new: assign next available ALU### ID, add to Alunos sheet
4. Mark as Processado

**For School Workshop submissions:**

1. Open "Inscrições Oficinas Escolas" sheet
2. Script pre-flags likely matches in `match_status`
3. Verify flagged matches
4. Confirm new students

---

## Creating the Forms

### Step-by-step:

1. Go to https://forms.google.com
2. Create new form
3. Add questions as specified above
4. Settings:
   - Collect email addresses: OFF
   - Limit to 1 response: OFF (families may have multiple kids)
   - Show progress bar: ON (for advanced form)
5. Link to response spreadsheet
6. Share form link

### QR Codes:

Create QR codes for each form for:
- Posters in schools
- WhatsApp sharing
- Events

Use: https://www.qr-code-generator.com/ or similar

---

## Integration with Database

The sync script will need a new function to:

1. Pull from "Novas Matrículas Avançado" where `status_processamento = Processado`
2. Pull from "Inscrições Oficinas Escolas" where `processado = Sim`
3. Insert/update students table with `program_type` field

Add to students table:
```sql
ALTER TABLE students ADD COLUMN program_type TEXT DEFAULT 'avancado';
-- Values: 'avancado', 'oficina', 'ambos'

ALTER TABLE students ADD COLUMN confirmed_2026 TEXT DEFAULT 'Não';
-- Values: 'Sim', 'Não', 'Evadido'
```
