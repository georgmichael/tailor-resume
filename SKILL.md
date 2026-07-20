---
name: tailor-resume
description: Rewrite a .docx resume's experience bullets to match a job description, asking the user for clarification only when a bullet lacks the info to align well, then output a new .docx with formatting preserved and optionally a matching cover letter. Use when the user provides a job description and wants their resume tailored.
---

# Tailor Resume

Rewrites each experience bullet in a Word resume to fit a target job description,
preserving the document's exact formatting, and outputs a new `.docx`.

Self-contained: the Python toolkit lives in `scripts/` next to this file and uses
a local venv at `.venv/` (created by `setup.sh`). The only dependency is
`python-docx` — no LibreOffice, no MCP, no network.

`$DIR` below = this skill's directory (the "Base directory for this skill" path).

## Setup (first run only)
If `$DIR/.venv` does not exist, run:
```
bash $DIR/setup.sh
```
This creates `$DIR/.venv` and installs `python-docx`. Use `$DIR/.venv/bin/python`
for all script calls below.

## Inputs to gather
1. The resume `.docx` path (ask the user if not provided).
2. The job description text (paste or file path).

## Workflow

### 1. Extract bullets
```
$DIR/.venv/bin/python $DIR/scripts/extract_bullets.py <resume.docx> --out /tmp/bullets.json
```
Read `/tmp/bullets.json`. Each entry has `id` (stable paragraph index), `context`
(the role/company header it falls under), and `text`. Some entries may be
non-experience lines (e.g. an Education line) — only rewrite real experience
bullets; leave the rest alone.

### 2. Rewrite, line by line, against the JD
For each experience bullet, rewrite it to align with the job description:
- Mirror the JD's language, priorities, and keywords (for ATS) where truthful.
- Lead with strong action verbs; quantify impact when the data exists.
- Keep roughly the original length so the layout/page-fit is unchanged.
- Stay within the role's `context` — don't invent responsibilities.
- Punctuation: never use em dashes, colons, or semicolons in a rewritten
  bullet. Rephrase into separate clauses or commas instead. (This applies only
  to the bullet text you write, not to these instructions.)

**Ask the user ONLY when needed.** If a bullet can be meaningfully tightened
toward the JD using info already present, just rewrite it. Pause and ask only
when a strong, JD-aligned rewrite genuinely requires facts you don't have —
e.g. a metric, a tool/technology the JD emphasizes, team size, or scope. Batch
such questions where possible; quote the bullet so the user has context. Apply
the answers, then continue.

Never fabricate metrics or experience. If the user can't supply a number,
rewrite qualitatively.

### 3. Name the output
The output base name is `{FirstName}{LastName}{CompanyName}Resume` — no spaces,
PascalCase, alphanumerics only (strip spaces/punctuation, e.g. `Jane Doe` +
`Acme, Inc.` → `JaneDoeAcmeIncResume`).
- Take the applicant's first/last name from the top of the resume.
- Take the company name from the job description; if it isn't stated there,
  ask the user for it.

### 4. Apply rewrites (formatting-safe) → new .docx
Write the approved rewrites to `/tmp/rewrites.json` as
`{"<id>": "<new text>", ...}` (omit bullets you left unchanged), then write the
new `.docx` next to the user's resume:
```
$DIR/.venv/bin/python $DIR/scripts/apply_rewrites.py <resume.docx> /tmp/rewrites.json --out <resume_dir>/{Base}.docx
```
The writer only edits text inside existing runs — paragraph styles, numbering,
indentation, fonts, and the manual bullet markers are left untouched. It never
adds, removes, or reorders paragraphs, so the layout is identical.

Deliver `<resume_dir>/{Base}.docx` to the user. They open it in Word or Google
Docs to make any minor fixes themselves.

### 5. Offer a cover letter
After delivering the new `.docx`, ask the user whether they would like a cover
letter tailored to the same job. If they decline, stop here.

If they accept, write a one-page cover letter and save it as an editable
`.docx` next to the resume named `{Base-without-"Resume"}CoverLetter.docx`
(e.g. `JaneDoeAcmeIncCoverLetter.docx`). Build it with `python-docx` using the
skill's venv, and also paste the full text in the reply. Rules:
- Draw every claim from the resume and the answers the user has already given.
  Never fabricate experience, metrics, or domain background.
- Mirror the JD's language and priorities, and lead with the strongest genuine
  overlap. If it is a stretch role, name the transferable strengths honestly
  and frame unfamiliar domains as something the applicant is eager to learn,
  rather than overclaiming.
- Pull the applicant's name and contact line from the top of the resume, and
  address the company/location/date from the JD. If a hiring manager name is
  unknown, use a neutral greeting and tell the user they can personalize it.
- Keep it to ~350-400 words (one page), 3-4 body paragraphs, and no em dashes.

## Guardrails
- Never add/remove/reorder paragraphs — ids must stay valid (text edits only).
- Don't touch headings, contact info, education, or non-experience sections
  unless the user asks.
- Preserve original bullet length where practical to avoid reflowing the page.
- No em dashes, colons, or semicolons in any rewritten bullet text.
- Never overwrite the user's original resume; always write a new `{Base}.docx`.
- If the user wants a PDF, the most faithful path is for them to open the
  `.docx` in their own Word/Google Docs and export it there — their renderer
  matches what reviewers will see. (We don't generate PDFs in this skill; some
  converters change the font line-metrics and inflate the page count.)
