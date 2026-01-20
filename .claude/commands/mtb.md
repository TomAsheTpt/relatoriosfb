# MTB Exam Import

Process an MTB (Music Teachers' Board) exam PDF from imports and generate a translated Portuguese report.

## Steps:

1. Look in `favelabrass/imports/` for any PDF files containing "MTB" in the filename
2. Read the PDF and extract all exam data:
   - Student name, instrument, grade level
   - Each piece name with accuracy/expression/technique scores
   - Scales and technical exercises scores (separately)
   - Reading and listening scores
   - All examiner comments
   - Final result and total score
3. Find or create the student in the database
4. Create/update the assessment record in `assessments_practical` with full breakdown
5. Translate the examiner comments to Portuguese and store both versions
6. Run `python3 favelabrass/data/generate_exam_report.py <assessment_id>` to generate the branded PDF
7. Move the original MTB PDF to `favelabrass/imports/processed/`

## Output:
- Branded PDF report in Portuguese at `favelabrass/outputs/`
- Database updated with full exam details
