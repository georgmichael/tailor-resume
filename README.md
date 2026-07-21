# Tailor Resume

**Give it your resume and a job posting. Get back a new resume rewritten to match that job, plus a matching cover letter, with your original formatting untouched.**

This is a tool that runs inside [Claude Code](https://claude.com/claude-code). You point it at your Word resume (`.docx`) and a job description, and Claude rewrites each of your experience bullet points to line up with what that job is asking for. It uses ATS-friendly keywords from the posting, keeps everything truthful, and only asks you a question when a bullet genuinely needs a detail it does not have (like a number or a tool you have used).

Your original resume is never changed. You always get a brand-new file.

---

## What you need before you start

1. **Claude Code** installed and working on your computer. If you do not have it yet, see https://claude.com/claude-code.
2. **Python 3** installed. Most Macs and Linux machines already have it. To check, open your Terminal and type `python3 --version`. If you see a version number, you are set. If not, download it from https://www.python.org/downloads/.
3. **Your resume as a Word file** (a `.docx` file). If yours is a PDF or Google Doc, open it and use "Save As" or "Download" to make a `.docx` copy first.

You do **not** need to know how to code. Claude handles the technical steps for you.

---

## Step 1: Install the tool

Open Claude Code, then type these two lines one at a time (press Enter after each):

```
/plugin marketplace add georgmichael/tailor-resume
```
```
/plugin install tailor-resume@georgmichael
```

The first line tells Claude where to find the tool. The second line installs it. You only do this once.

> **Prefer not to use the plugin system?** See ["Other ways to install"](#other-ways-to-install) near the bottom.

---

## Step 2: Use it

In Claude Code, type:

```
/tailor-resume
```

Then give Claude two things (it will ask if you forget):

1. **Your resume** — drag the `.docx` file in, or paste the full path to it (for example `/Users/yourname/Downloads/MyResume.docx`).
2. **The job description** — paste the text of the posting, or just paste a link to it.

That is it. Claude will:

- Read every experience bullet on your resume.
- Rewrite each one to match the job, using the posting's own wording where it is truthful.
- Pause to ask you a question **only** if a bullet could be much stronger with a fact it does not have (like "how many users?" or "did you use Excel here?"). You can always answer "I don't have that," and it will rewrite without inventing anything.
- Save a **new** resume next to your original, named like `JaneDoeAcmeResume.docx`.
- Offer to also write a **one-page cover letter** for the same job. Say yes and it saves `JaneDoeAcmeCoverLetter.docx` in the same place.

---

## Step 3: Review and send

Open the new file in Word or Google Docs, read it over, and make any small tweaks you like. When you are happy with it:

- **To send a PDF:** open the `.docx` in Word or Google Docs and use "Export" or "Download as PDF" from there. That gives the most reliable page layout.

---

## Frequently asked questions

**Will it change my original resume?**
No. It always writes a new file and leaves your original exactly as it was.

**Will it make up experience or fake numbers?**
No. It only uses what is already on your resume and the answers you give it. If it needs a detail to make a bullet stronger, it asks you first.

**Will the layout or formatting get messed up?**
No. It only swaps the words inside your existing bullets. Fonts, spacing, bullet points, and page layout stay the same.

**Do I have to answer a bunch of questions every time?**
Usually not. It only asks when a bullet genuinely needs a fact to align well with the job. Many resumes need zero questions.

**Something went wrong / it mentions a "venv" or "python-docx."**
The very first time you use it, Claude sets up a small helper environment automatically (this needs Python 3 installed, see above). If you see an error, tell Claude "the setup failed" and it will walk you through it.

---

## Update or remove it later

- **Update to the newest version:** type `/plugin update tailor-resume@georgmichael` in Claude Code.
- **Remove it:** type `/plugin uninstall tailor-resume@georgmichael`.

---

## Other ways to install

If you would rather not use the plugin system, you can copy the tool in by hand. Download or clone this repository into one of these folders:

- Just for you, everywhere: `~/.claude/skills/tailor-resume/`
- Shared inside a specific project: `<your-project>/.claude/skills/tailor-resume/`

Then use `/tailor-resume` the same way. The one-time setup still runs automatically on first use, and Python 3 is still the only requirement.

---

## For the curious: how it works

Claude provides the writing and judgment. A couple of small bundled Python scripts do the mechanical, formatting-safe parts so nothing in your document shifts.

- `SKILL.md` — the instructions Claude follows.
- `scripts/extract_bullets.py` — finds your experience bullets and tags each with a stable id and the role it belongs to.
- `scripts/apply_rewrites.py` — writes the new wording back in, editing only the text inside your existing bullets so styles, numbering, fonts, and indentation are left untouched.
- `requirements.txt`, `setup.sh` — the single dependency (`python-docx`) and the one-time environment setup.

License: [MIT](LICENSE). You are free to use, change, and share it.
