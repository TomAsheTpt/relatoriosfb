# Favela Brass Data Architecture

Design principles and table structures for the SQLite database in HQ.

---

## How It Works

**Staff work in Google Sheets** (their source of truth) → **Tom exports CSVs** to `/imports` → **Claude imports to SQLite** → **Reports and analysis from HQ**

Staff never see the database. They see beautiful outputs.

---

## Core Design Principles

### Normalized Relational Design
- **One master Students table** with stable identity fields (name, DOB, gender, ID)
- **Linked tables** for one-to-many relationships (attendance, assessments, instruments, enrolments)
- Foreign keys to link tables (student_id, group_id, etc.)
- Avoid over-fragmentation - don't split 1:1 data into separate tables

### Practical Rules
- Keep "one-to-one" data in main tables (address, guardian contact)
- Use linked tables only for "one-to-many" or "many-to-many" data
- When importing CSVs, match on student name or ID to link records

---

## Core Tables

### Students (Alunos)
The master table - one row per human.
- `student_id` (primary key)
- `name`
- `date_of_birth`
- `gender`
- `status` (Active / Inactive / Graduated)
- `type` (School / Favela / Both)
- `school` (current)
- `community` (favela/neighborhood)
- `guardian_name`
- `guardian_phone`
- `join_date`

### Student_Year
Annual snapshot for data that changes year-to-year (avoids editing history):
- `student_id` (FK)
- `year`
- `school` (that year)
- `address`
- `t_shirt_size`
- `guardian_contacts`
- `confirmed_on` (date)
- `confirmed_by`

---

## Program Structure

### Programmes / Activities
Defines what the "thing" is:
- `programme_id`
- `name` ("School - Beginners", "Favela - Advanced", "Private Lessons", "Theory", "Rehearsal")
- `type` (Private Lesson / Rehearsal / Theory / School Class)
- `counts_towards_attendance` (yes/no)

### Groups (Turmas)
The roster container - "Tuesdays 16:00 at Escola X with Teacher Y":
- `group_id`
- `programme_id` (FK)
- `teacher`
- `location` (school/favela site)
- `day_time_pattern`
- `term_start` / `term_end`
- `roster_type` (Group / 1:1)
- `active` (yes/no)

### Enrolments
Student joins a turma (can leave later):
- `enrolment_id`
- `student_id` (FK)
- `group_id` (FK)
- `start_date`
- `end_date`
- `instrument` (at that time)
- `notes`

---

## Attendance System

### Sessions
Each actual occurrence of a class:
- `session_id`
- `group_id` (FK)
- `datetime`
- `status` (Held / Cancelled / Holiday / Make-up)
- `notes`

### Attendance
One row per student per session:
- `attendance_id`
- `session_id` (FK)
- `student_id` (FK)
- `teacher_mark` (Present / Absent) - what teacher knows immediately
- `absence_classification` (Unclassified / Authorised / Unauthorised) - decided later by admin
- `recorded_by`
- `recorded_at`
- `notes`

**Workflow:**
1. Teachers mark Present/Absent only
2. Default everyone to Present (teachers tap the 2-6 absences)
3. Lillian classifies absences later via "Absences pending authorisation" view
4. Final status derived: Present / Authorised Absence / Unauthorised Absence / Pending

**Favela Course Specifics:**
Students have 3 streams (1:1 lesson + rehearsal + theory) - monthly attendance is aggregate of all three.

---

## Assessments

### Assessments
- `assessment_id`
- `student_id` (FK)
- `date`
- `category` (Prática / Teoria)
- `type` (Interna / Externa)
- `level_tested` (Nível 1-6)
- `instrument`
- Score components (varies by category):
  - `score_piece_1`, `score_piece_2`, `score_piece_3`
  - `score_scales_arpeggios`
  - `score_sight_reading`
  - `score_technical_exercises`
  - `score_aural`
- `total_score`
- `result_calculated` (auto from score)
- `result_manual_override` (optional)
- `result_final` (= override if exists, else calculated)
- `certificate_issued` (yes/no)
- `certificate_date`
- `assessor`
- `notes`

**Result Logic:**
- Distinção / Mérito / Aprovado / Reprovado
- Teoria needs its own scoring model (separate from Prática)

---

## Instruments

### Instruments
- `instrument_id`
- `type` (Trumpet, Trombone, etc.)
- `serial_number`
- `status` (In Use / In Storage / Under Repair / Retired)
- `last_inspection`
- `notes`

### Instrument_Assignments
- `assignment_id`
- `instrument_id` (FK)
- `student_id` (FK)
- `date_out`
- `due_back`
- `date_in`
- `condition_out`
- `condition_in`

**Anomaly Views to Maintain:**
1. Students in a band but with no active instrument
2. Students holding multiple instruments simultaneously
3. Instruments assigned to multiple students
4. Assignments overdue for return
5. Inactive student still holding instrument
6. Instruments unassigned but not "In Storage"
7. Duplicate serial numbers
8. Inspection overdue (>6 months)

---

## Events

### Events
- `event_id`
- `name`
- `date`
- `type` (Performance / Workshop / Meeting / etc.)
- `location`
- `status`
- `notes`

### Event_Participants
- `event_id` (FK)
- `student_id` (FK) or `staff_id`
- `role` (Performer / Helper / etc.)

---

## Bands

### Bands
- `band_id`
- `name` (Banda Roxa, Banda Amarela, Banda Verde, etc.)
- `level`
- `active` (yes/no)

### Band_Memberships
- `student_id` (FK)
- `band_id` (FK)
- `start_date`
- `end_date`
- `instrument` (in this band)

---

## Repertoire

### Pieces
- `piece_id`
- `title`
- `composer_arranger`
- `difficulty_level`
- `duration`
- `youtube_link`
- `score_pdf_link`

### Band_Repertoire
- `band_id` (FK)
- `piece_id` (FK)
- `status` (Learning / Performance Ready / Retired)
- `date_introduced`

---

## Financial (if needed)

### Transactions
- `transaction_id`
- `date`
- `description`
- `amount`
- `category`
- `account` (Principal / Rouanet / etc.)
- `lei_rouanet_item` (for compliance)

---

## Key Formulas / Derived Fields

### Student Level
- Active Assignments Count
- In A Band? (yes/no)
- Current Instrument
- Monthly Attendance Rate
- Latest Assessment Result

### Instrument Level
- Active Assignee Count
- Days Since Last Inspection
- Is Overdue?

### Session Level
- Attendance Rate (Present / Total Enrolled)
- Absences Pending Classification Count

---

## Import Workflow

### Expected CSV Sources (from Google Sheets)
- **Students master list** - exported periodically
- **Attendance records** - monthly or as needed
- **Assessment results** - after exam periods
- **Instrument inventory** - when updated
- **Event logs** - as events happen

### Import Process
1. Staff update Google Sheets
2. Tom exports CSV to `/imports`
3. Claude validates and imports to SQLite
4. Processed CSVs moved to `/imports/processed`
5. Claude can then query, analyze, generate reports

### Data Quality Checks on Import
- Validate student names match existing records (or flag new students)
- Check for duplicates
- Verify required fields present
- Flag anomalies for review
