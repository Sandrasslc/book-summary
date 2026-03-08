# book-summary

A SoloEnt skill that generates structured Markdown reading notes from local book files (TXT or MD). Point it at a file and it returns chapter summaries, key insights, memorable quotes, and a full highlights section.

> **Disclaimer:** By using this skill, you confirm that you own or have obtained the legal right to access, reproduce, and analyze the book file provided. Do not use this tool on copyrighted material without proper authorization. The authors of this tool accept no responsibility for copyright infringement or unauthorized use of third-party content.

## Requirements

- [Soloent](https://soloent.ai) with Skills enabled
- Python 3 (for the chapter-analysis helper script)

## Install

```bash
git clone https://github.com/Sandrasslc/book-summary.git ~/skills/book-summary
bash ~/skills/book-summary/install.sh
```

The installer will ask whether to install globally (`~/.soloent/skills/`) or for the current project only (`.soloent/skills/`). Global is recommended so the skill is available in every project.

**Manual install** — copy the skill directory to your preferred location:

```bash
# Global
cp -r ~/skills/book-summary/.soloent/skills/book-summary ~/.soloent/skills/

# Project-level
cp -r ~/skills/book-summary/.soloent/skills/book-summary /your/project/.soloent/skills/
```

## Usage

In SoloEnt, type:

```
/book-summary /path/to/book.txt
/book-summary /path/to/book.md
```

Soloent will:
1. Detect encoding and scan the book structure
2. List all chapters found
3. Ask which chapters to summarize (if more than 10)
4. Extract and analyze each chapter
5. Write a `book-notes-[title]-[date].md` file

## Output format

```markdown
# Reading Notes: *Book Title*

## I. Book Overview
## II. Chapter Summaries
## III. Book Highlights     ← TOP 5 ideas, TOP 10 quotes
## IV. Personal Reflections
## V. Chapter Index
```

## Skill structure

```
.soloent/skills/book-summary/
├── SKILL.md                  # Main instructions loaded by Soloent
├── docs/
│   └── chapter-patterns.md   # Regex patterns for chapter detection
├── scripts/
│   └── analyze-book.py       # Helper: info / chapters / extract commands
└── templates/
    └── note-template.md      # Output template
```

### `analyze-book.py` commands

| Command | Description |
|---------|-------------|
| `python3 analyze-book.py <file> info` | Show title, encoding, line count, chapter count |
| `python3 analyze-book.py <file> chapters` | List all chapter headings with line numbers |
| `python3 analyze-book.py <file> extract <start> <end>` | Extract lines between `start` and `end` |

## Supported chapter formats

- English: `Chapter 1`, `Part I`, `Section 2`
- Chinese: `第一章`, `第1回`, `第三节`
- Numbered: `1.`, `2.`, `一、`, `二、`

## License

MIT
