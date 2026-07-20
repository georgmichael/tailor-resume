# tailor-resume

A Claude Code skill that rewrites a Word resume's experience bullets to match a
job description, preserving the document's exact formatting, and outputs a new
`.docx`.

Claude does the language and judgment (and asks you for missing facts only when a
bullet needs them); the bundled Python scripts do the formatting-safe mechanics.

## Install
Copy this `tailor-resume/` folder into a Claude Code skills directory:
- Personal (all your projects): `~/.claude/skills/tailor-resume/`
- Project (shared with a repo): `<repo>/.claude/skills/tailor-resume/`

That's it — Claude runs the one-time `setup.sh` (creates a local venv, installs
`python-docx`) on first use. Only requirement: `python3`.

## Use
In Claude Code:
```
/tailor-resume
```
Then give it your resume `.docx` and the job description (paste or a URL). It
walks each experience bullet, rewrites toward the JD, asks only when a bullet
genuinely lacks a fact, and writes a new `{First}{Last}{Company}Resume.docx`
next to your original. Your original file is never modified.

After the tailored resume is written, it offers to generate a matching one-page
cover letter (saved as `{First}{Last}{Company}CoverLetter.docx`), built only
from facts already in your resume and the answers you gave.

For a PDF, open the output `.docx` in Word or Google Docs and export it there —
your own renderer matches what reviewers see.

## Files
- `SKILL.md` — the skill instructions Claude follows.
- `scripts/extract_bullets.py` — finds experience bullets, emits stable ids + role context.
- `scripts/apply_rewrites.py` — writes rewritten text back, editing only text inside
  existing runs so styles/numbering/fonts/indentation are untouched.
- `requirements.txt`, `setup.sh` — dependency + one-time environment setup.
