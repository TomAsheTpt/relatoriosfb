# Google Sheets Structure for Favela Brass

## Overview

Staff edit Google Sheets → Daily sync → SQLite database → Reports/analysis

Each sheet has:
- **Protected header row** (staff can't break column names)
- **Data validation** where possible (dropdowns, date formats)
- **Clear column names** in Portuguese

---

## Sheet 1: Alunos (Students)

**Who updates:** Iris, Lillian
**Frequency:** When students enroll, leave, or info changes

| Column | Type | Validation | Notes |
|--------|------|------------|-------|
| id | Auto | Protected | `ALU001`, `ALU002`, etc. |
| nome | Text | Required | Full name |
| data_nascimento | Date | DD/MM/YYYY | |
| genero | Dropdown | M / F | |
| comunidade | Text | | Which community they live in |
| mora_em_comunidade | Dropdown | Sim / Não | |
| escola | Text | | Current school |
| data_matricula | Date | DD/MM/YYYY | When they joined FB |
| status | Dropdown | Ativo / Evadido / Ex-Aluno | |
| data_saida | Date | DD/MM/YYYY | If they left |
| motivo_saida | Dropdown | From exit_reasons | |
| tamanho_uniforme | Dropdown | PP/P/M/G/GG/XGG | |
| autorizacao_imagem | Dropdown | Sim / Não | |
| necessidades_especiais | Text | | |
| condicao_medica | Text | | |
| observacoes | Text | | General notes |

---

## Sheet 2: Instrumentos (Inventory)

**Who updates:** Wesley, teachers
**Frequency:** When instruments acquired, repaired, written off

| Column | Type | Validation | Notes |
|--------|------|------------|-------|
| id | Number | Protected | FB inventory number (1, 2, 3...) |
| tipo | Dropdown | From instrument_types | Trompete, Trombone, etc. |
| marca_modelo | Text | | Brand and model |
| numero_serie | Text | | Serial number |
| qualidade | Dropdown | Bom / Regular / Ruim | |
| tem_case | Dropdown | Sim / Não | |
| baixado | Dropdown | Sim / Não | Written off? |
| motivo_baixa | Text | | If written off, why |
| anotacoes | Text | | Donor info, quirks, etc. |

---

## Sheet 3: Emprestimos (Loans)

**Who updates:** Iris, Wesley
**Frequency:** When instruments lent or returned

| Column | Type | Validation | Notes |
|--------|------|------------|-------|
| id | Auto | Protected | `EM001`, `EM002`, etc. |
| instrumento_id | Number | Must exist in Instrumentos | FB inventory number |
| aluno_nome | Text | Should match Alunos.nome | |
| categoria | Dropdown | Aluno / Ex-aluno / Professor | |
| data_emprestimo | Date | DD/MM/YYYY | |
| data_devolucao | Date | DD/MM/YYYY | Expected return |
| status | Dropdown | Ativo / Devolvido | |
| obs | Text | | |

---

## Sheet 4: Avaliacoes (Assessments)

**Who updates:** Wesley, teachers after exams
**Frequency:** After each assessment period (2x per year)

| Column | Type | Validation | Notes |
|--------|------|------------|-------|
| id | Auto | Protected | `AV001`, etc. |
| aluno_nome | Text | Should match Alunos.nome | |
| data | Date | DD/MM/YYYY | |
| tipo | Dropdown | Interna / Externa | |
| categoria | Dropdown | Prática / Teoria | |
| nivel_testado | Number | 1-4 | |
| instrumento | Dropdown | From instrument_types | |
| pontuacao_peca_1 | Number | 0-20 | |
| pontuacao_peca_2 | Number | 0-20 | |
| pontuacao_peca_3 | Number | 0-20 | |
| pontuacao_escalas | Number | 0-20 | |
| pontuacao_leitura | Number | 0-20 | |
| pontuacao_tecnica | Number | 0-20 | |
| pontuacao_teoria | Number | 0-10 | For theory exams |
| pontuacao_final | Number | Calculated | =SUM or manual |
| resultado | Dropdown | Distinção / Mérito / Aprovado / Reprovado | |
| avaliador | Text | | Examiner name |
| observacoes | Text | | |

---

## Sheet 5: Bandas (Bands) - Reference Only

**Who updates:** Tom only
**Frequency:** Rarely (semester changes)

| Column | Type | Notes |
|--------|------|-------|
| id | Text | banda_001, etc. |
| nome | Text | Banda Preta, Banda Roxa, etc. |
| regente | Text | Conductor name |
| ativa | Sim/Não | |
| tamanho_previsto | Number | Target size |
| descricao | Text | |

---

## Sheet 6: Atribuicao_Bandas (Band Assignments)

**Who updates:** Wesley, Tom
**Frequency:** Each semester

| Column | Type | Validation | Notes |
|--------|------|------------|-------|
| id | Auto | Protected | |
| aluno_nome | Text | Must match Alunos | |
| banda_atual | Dropdown | From Bandas | |
| instrumento | Dropdown | From instrument_types | |
| data_inicio | Date | DD/MM/YYYY | |
| banda_proxima | Dropdown | From Bandas | Projected next semester |
| ano_formatura | Number | | Expected graduation year |

---

## Sheet 7: Professores (Teachers) - Reference Only

**Who updates:** Tom, Raíssa
**Frequency:** When staff changes

| Column | Type | Notes |
|--------|------|-------|
| nome | Text | |
| funcao | Text | Professor, Regente, etc. |
| situacao | Dropdown | Ativo / Inativo / Em Experiência |
| valor_hora | Number | R$ per hour |
| instrumentos | Text | What they teach |

---

## Sheet 8: Atividades (Schedule/Timetable)

**Who updates:** Tom, Wesley
**Frequency:** Each semester

| Column | Type | Notes |
|--------|------|-------|
| id | Auto | |
| dia_semana | Dropdown | Segunda, Terça, etc. |
| nome | Text | Activity name |
| tipo | Dropdown | ensaio_banda, aula_individual, etc. |
| horario_inicio | Time | HH:MM |
| horario_fim | Time | HH:MM |
| local | Text | Casa Tom, Curvelo, etc. |
| professor | Text | |

---

## Sheets NOT needed (derived/calculated):

- **Reparos** → Could be a sub-sheet or just notes on Instrumentos
- **Cálculo Mensal** → Generated from Atividades + Professores
- **Progresso dos Alunos** → Derived from Avaliacoes + Atribuicao
- **Promoções** → Log in Atribuicao_Bandas history

---

## Sync Rules

1. **IDs are sacred** - never delete/change ID column
2. **Names must match** - `aluno_nome` in Emprestimos must exactly match `nome` in Alunos
3. **Dates in DD/MM/YYYY** - script converts to ISO for SQLite
4. **Empty cells = NULL** - that's fine
5. **Deleted rows** - sync script marks as deleted, doesn't hard delete from SQLite (audit trail)

---

## Permissions

| Sheet | Iris | Lillian | Wesley | Teachers | Raíssa |
|-------|------|---------|--------|----------|--------|
| Alunos | Edit | Edit | View | View | View |
| Instrumentos | View | - | Edit | Edit | - |
| Emprestimos | Edit | - | Edit | View | - |
| Avaliacoes | View | - | Edit | Edit | - |
| Bandas | View | View | View | View | View |
| Atribuicao_Bandas | View | - | Edit | View | - |
| Professores | View | - | View | View | Edit |
| Atividades | View | - | Edit | View | - |
