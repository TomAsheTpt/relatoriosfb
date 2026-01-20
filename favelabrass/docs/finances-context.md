# Favela Brass Finances Context

## Account Structure

Favela Brass operates multiple bank accounts:

| Account | Purpose |
|---------|---------|
| **BB Associação** (Conta Principal) | Day-to-day operations, receives donations, pays expenses |
| **BB Rouanet** | Lei Rouanet project funds – restricted use |
| **CDB/Investments** | Reserves parked in CDB |
| **PayPal** | International donations, flows to BB Associação |
| **Caixinha** | Petty cash, operated via Tom's personal account |

## How Money Flows

```
Donors/Sponsors → Rouanet Account → Project Expenses
                                  → Reimbursements to Associação

Donations (PayPal, Pix) → Associação Account → Operations
Shows/Sales revenue → Associação Account → Operations

Associação ←→ Rouanet (reimbursements when Associação fronts expenses)
```

## Lei Rouanet Project

- **Plano Anual** – annual plan approved by government
- **2025 Budget Approved:** R$ 2.07M
- **2025 Captured:** ~R$ 1M (funds actually raised from sponsors)
- **2025 Executed:** ~R$ 1M (100% of captured funds spent)

### Budget Categories (Rouanet)
- Equipe Técnica (staff salaries)
- Professores (teacher salaries)
- Alimentação (student meals/snacks)
- Transporte
- Comunicação (15% cap)
- Administração (10% cap)
- Instrumentos/Equipamento
- Uniformes
- Hospedagem
- Acessibilidade

### Rules
- Can move money between budget lines (remanejamento) with justification
- Max 20% can go to proponent organization (Associação)
- Must justify in Prestação de Contas (annual accountability report)

## Timing Issues

Rouanet funds don't always arrive on schedule. In 2025:
- **January:** SALIC account issues – Associação covered expenses
- **October-November:** Funds delayed – Associação covered expenses
- **December:** Final reimbursement arrived, replenished Associação

This causes cash flow volatility – Associação balance swings dramatically based on Rouanet timing.

## Consolidation Rules

When combining Associação + Rouanet for reporting:

1. **Don't double-count reimbursements** – money flowing from Rouanet to Associação is internal
2. **Rouanet "Total Utilizado"** includes expenses paid via Associação (same salaries, different payment route)
3. **Associação "Prestação de Serviços - Projetos"** income is often the Rouanet admin fee – don't count as separate external income
4. **Associação "Transferências"** category = Rouanet reimbursements received

### Income Sources (Consolidated)
- **Grant funding:** Lei Rouanet
- **Earned income:** Shows, Vendas (actual external revenue)
- **Donations:** Recorrentes + Pontuais
- **Other:** Rendimentos financeiros (CDB interest)

## Key People

| Person | Role | Notes |
|--------|------|-------|
| Wesley | Diretor Musical | |
| Tom | Coordenação Geral / Direção Artística | Also manages Caixinha |
| Iris | Coord. Pedagógica | Data quality |
| Raíssa | Coord. Administrativa | Maintains all finance spreadsheets |
| Carol | Produtora Executiva | |
| Rafael | Comunicação | |
| Wellington | Produtor Local | |
| Lilian | Assistente Social | |

## Data Sources

Raíssa maintains in Google Sheets:
- `Planilha de Execução Associação 2025` – monthly tabs for BB Associação transactions
- `Planilha de Execução Rouanet 2025` – Rouanet budget tracking
- Cash flow summary (Fluxo de Caixa)
- Budget vs Actual (Previsão + Executado)

Export as CSV → drop in `/imports` → Claude processes into database.

## Database Schema

```
favelabrass.db
├── transactions
│   - date, year, month
│   - amount, category, description
│   - is_income, is_caixinha, is_internal_transfer
│   - account, source_file
│
└── monthly_balances
    - year, month
    - cdb_opening, cc_opening, paypal_opening, caixinha_opening
    - cdb_closing, cc_closing, paypal_closing, caixinha_closing
    - income, expenses, net_flow
```

## 2025 Summary

| Metric | Value |
|--------|-------|
| Total Income | R$ 1.17M |
| Total Expenses | R$ 1.12M |
| Net Result | +R$ 50k surplus |
| Lei Rouanet % of income | 86% |
| People costs % of expenses | 66% |
| Students served | ~250 |

## Recommendations for 2026

1. Keep Associação/Rouanet sheets separate (operational reasons)
2. Standardize column format (no R$ prefix, consistent headers)
3. Add "Reimbursement Status" column to Associação for Rouanet-related expenses
4. Monthly CSV exports to `/imports`
5. Monthly balance reconciliation with bank statements
