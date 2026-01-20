# Favela Brass Slack Bot Specification

## Overview

Slack bot providing staff UI for querying and updating the SQLite database.

**Infrastructure:**
- Cloud VPS (DigitalOcean São Paulo, ~R$40/month)
- SQLite database synced from HQ
- Python bot using Slack Bolt SDK
- Git backup on every write

---

## Query Commands (read-only)

### `/aluno <id or name>`
```
/aluno 139
→ 📋 João Pedro Ferreira Martins (139)
  🎵 Banda Verde | Sax Tenor
  📚 teoria_n2_pablo
  🎹 Aula: Joana, Ter 18:00-18:30 Casa Tom
  🎺 Empréstimo: Sax Tenor IN087
  📍 Comunidade: Pereira da Silva

/aluno maria
→ 8 resultados para "maria":
  213 Maria Antônia M. - Preta - Sax Tenor
  214 Maria Antonia N. - Roxa - Trombone
  ...
```

### `/banda <nome>`
```
/banda preta
→ 🎷 Banda Preta (21 alunos)

  Trompetes (6): Aryelle, Heron, Lucia, Marcelo, Marcos Felipe, Rafael S.
  Trombones (5): Alex, Edileuza, Ingrid, Juan, Maria Eduarda
  Saxofones (5): Davi, Emilly V., Maria Antônia M., Maria Rita, Ryan P.
  Percussão (5): Barbara, Elisabete, Felipe, Luiz Henrique, Maria Helena
```

### `/horario <professor> [dia]`
```
/horario joana
→ 🎹 Joana Saraiva - 16 aulas

  Segunda (Silvia):
  18:00-18:30 Emilly Vitória
  18:30-19:00 Ryan Cantoni
  ...

/horario shanso sabado
→ 🎹 Shanso Araújo - Sábado (Zola)
  09:30-10:00 Cesar Augusto
  10:00-10:30 Isac Nunes
  ...
```

### `/instrumento <id>`
```
/instrumento IN087
→ 🎺 IN087 - Sax Tenor Yamaha YTS-280
  Estado: Bom
  Emprestado: João Pedro (139)
  Desde: 15/03/2025
```

### `/teoria <grupo>`
```
/teoria n2_pablo
→ 📚 Teoria Nível 2 - Pablo (12 alunos)
  Carlos Henrique, Emilly Vitória, Gustavo, João Pedro, ...
```

### `/busca <termo>`
```
/busca trompete amarela
→ 🔍 8 resultados:
  21 Ana Laura - Banda Amarela - Trompete
  38 Arthur Bezerra - Banda Amarela - Trompete
  ...
```

---

## Update Commands (write - with confirmation)

All updates require ✅ reaction to confirm.

### Lesson changes
```
ATUALIZAÇÃO: 139 aula mudar Ter 19:00 SV

→ 🔄 Mudança solicitada:
  João Pedro - aula com Joana
  De: Ter 18:00 Casa Tom
  Para: Ter 19:00 Silvia

  ✅ Sem conflitos
  Reagir ✅ para confirmar
```

### Status changes
```
ATUALIZAÇÃO: 139 saiu - desmotivação

→ 🚨 Mudança de status:
  João Pedro (139)
  Ativo → Evadido
  Motivo: desmotivação

  Isso vai:
  • Cancelar aula com Joana
  • Registrar saída em Saidas
  • Solicitar devolução IN087

  Reagir ✅ para confirmar
```

### Instrument loans
```
ATUALIZAÇÃO: IN045 emprestado 283

→ 🎺 Empréstimo:
  IN045 (Trompete Jupiter) → Rafael Alves (283)

  Reagir ✅ para confirmar
```

### Band changes
```
ATUALIZAÇÃO: 139 promovido Banda Roxa

→ 🎵 Promoção:
  João Pedro (139)
  Banda Verde → Banda Roxa

  Reagir ✅ para confirmar
```

---

## Admin Commands (Tom only)

### `/backup`
```
→ ✅ Backup criado: favelabrass-2026-01-20-0830.db
  Git commit: a3f2b1c
```

### `/rollback`
```
→ ⚠️ Último commit: "2026-01-20: moved João, marked Maria evadido"
  3 mudanças serão desfeitas

  Reagir ✅ para confirmar rollback
```

### `/log [n]`
```
/log 5
→ 📜 Últimas 5 mudanças:
  20/01 08:30 - João (139) aula movida Ter 19:00
  20/01 08:28 - Maria (226) marcada Evadido
  ...
```

---

## Daily Digest (automated, 08:00)

```
📊 Resumo Diário - 20 Jan 2026

Ontem:
✅ 4 atualizações processadas
⚠️ 1 pendente de confirmação

Pendente:
• "139 mudar aula Qua" - conflito não resolvido

Alertas:
• IN045 com reparo pendente há 14 dias
• 3 alunos sem aula atribuída
```

---

## Staff Reference (pinned in Slack)

74 advanced course students with IDs - see `/aluno list` or pinned message.

**Location codes:**
- CT = Casa Tom
- SV = Silvia (Terraço)
- ZL = Pizzaria Zola
- CV = Curvelo

**Update format:**
```
ATUALIZAÇÃO: <student_id> <change>
```

---

## Technical Notes

- Bot runs on DigitalOcean VPS (São Paulo)
- Python + Slack Bolt SDK
- SQLite database (same as HQ)
- Git commit after each confirmed write
- Auto-restart on crash via systemd
- Nightly backup to Tom's machine

---

## What Slack WON'T Handle

These still need spreadsheet imports:

1. **New student enrollments** - too many fields
2. **Start-of-year band assignments** - bulk visual layout
3. **MTB exam imports** - CSV from external system
4. **Daily attendance** - needs proper checkbox UI
5. **Complex assessments** - too many score fields

---

## Outstanding Items (Jan 2026)

Before bot is live:

1. [ ] Create Slack app and get bot token
2. [ ] Build basic query commands locally
3. [ ] Test with Tom
4. [ ] Deploy to VPS
5. [ ] Add update commands
6. [ ] Train staff on format
