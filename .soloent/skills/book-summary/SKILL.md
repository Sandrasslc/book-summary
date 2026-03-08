---
name: book-summary
description: Generate structured Markdown reading notes from local book files (TXT/MD). Use when asked to "summarize a book", "break down a book", "take reading notes", "extract quotes", or "make book notes" from a file.
---

# Book Summary

Generate structured reading notes from a local book file — chapter summaries, key insights, memorable quotes, and a full highlights section.

> **Disclaimer:** By using this skill, you confirm that you own or have obtained the legal right to access, reproduce, and analyze the book file provided. Do not use this tool on copyrighted material without proper authorization. The authors of this tool accept no responsibility for copyright infringement or unauthorized use of third-party content.

## Usage

```
/book-summary /path/to/book.txt
/book-summary /path/to/book.md
```

## Step 1 — Analyze the Book

Run the info command to detect encoding, count lines, and preview the file:

```bash
python3 scripts/analyze-book.py <file_path> info
```

Expected output:
```
Title: The Lean Startup
File: the-lean-startup.txt
Encoding: utf-8
Total lines: 4821
Chapters: 14

=== Beginning of File ===
The Lean Startup
Eric Ries
...
```

## Step 2 — List All Chapters

```bash
python3 scripts/analyze-book.py <file_path> chapters
```

Expected output:
```
  1. [line   102] Chapter 1: Start
  2. [line   310] Chapter 2: Define
  3. [line   519] Chapter 3: Learn
```

## Step 3 — Confirm Scope with User

If there are more than 10 chapters, ask the user before proceeding:

> Found 18 chapters. Which would you like me to summarize?
> - [ ] All chapters
> - [ ] A range (e.g., chapters 1–5)
> - [ ] Core chapters only (I'll pick the most important)

## Step 4 — Extract and Analyze Each Chapter

Extract chapter content by line range:

```bash
python3 scripts/analyze-book.py <file_path> extract <start_line> <end_line>
```

For each chapter, extract:
- **Core summary** – 2–3 sentences
- **Key insights** – 3–5 bullet points
- **Memorable quotes** – verbatim, using `>` blockquote format

## Step 5 — Write the Notes File

Use [templates/note-template.md](templates/note-template.md) as the output structure.

Save as: `book-notes-[title]-[YYYY-MM-DD].md`

## Large File Strategy

Books over 2000 lines are processed in chunks — never read the whole file at once.

| Phase | Action |
|-------|--------|
| Scan | Read first 500 lines to identify structure |
| Locate | Find all chapter headings and line numbers |
| Extract | Read one chapter at a time using `offset/limit` |

Chapter pattern reference: [docs/chapter-patterns.md](docs/chapter-patterns.md)

## Rules

- Quotes must be **verbatim** — never paraphrase a quote
- Use `>` blockquote format for all quotes
- Stay objective — reflect the author's intent, not your interpretation
- Confirm scope with the user before processing more than 10 chapters
