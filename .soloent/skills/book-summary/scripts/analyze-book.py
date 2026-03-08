#!/usr/bin/env python3
"""
Book file preprocessing script.
Analyzes long-text books, extracts chapter structure,
and avoids loading the entire file into context at once.

DISCLAIMER: By using this script, you confirm that you own or have obtained
the legal right to access, reproduce, and analyze the book file provided.
Do not use this tool on copyrighted material without proper authorization.
The authors of this tool accept no responsibility for copyright infringement
or unauthorized use of third-party content.
"""

import re
import sys
import os
from pathlib import Path

def detect_encoding(file_path):
    """Detect file encoding."""
    encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'utf-16']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1024)
                return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    return 'utf-8'

def find_chapters(file_path, encoding='utf-8'):
    """Locate all chapter headings and their line numbers."""

    # Chapter recognition patterns
    patterns = [
        # Chinese: 第一章、第1回、第二十三章
        r'^第[一二三四五六七八九十百千零\d]+[章回节部卷]',
        # English: Chapter 1, Part I
        r'^(Chapter|Part|Section)\s+[\dIVX]+',
        # Numbered: 1. 2. 3.
        r'^\d+[\.\、]\s+.+',
        # Chinese ordinals: 一、二、三、
        r'^[一二三四五六七八九十]+[、\.]\s+.+',
    ]

    combined_pattern = '|'.join(f'({p})' for p in patterns)
    chapter_regex = re.compile(combined_pattern, re.IGNORECASE)

    chapters = []

    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line and chapter_regex.match(line):
                chapters.append({
                    'line': line_num,
                    'title': line[:100]  # Limit title length
                })

    return chapters

def get_book_info(file_path, encoding='utf-8', sample_lines=50):
    """Extract basic book information from the beginning of the file."""

    info = {
        'filename': os.path.basename(file_path),
        'total_lines': 0,
        'title': None,
        'author': None,
        'first_lines': []
    }

    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        lines = []
        for i, line in enumerate(f):
            if i < sample_lines:
                lines.append(line.strip())
            info['total_lines'] = i + 1

    info['first_lines'] = lines

    # Attempt to extract the book title from the filename or beginning of file
    name = Path(file_path).stem
    # Remove common suffixes
    name = re.sub(r'[\-_]?(读书笔记|摘要|精华|节选|全集|完整版).*$', '', name)
    info['title'] = name

    return info

def extract_chapter_content(file_path, start_line, end_line, encoding='utf-8'):
    """Extract content within a specified line range."""

    lines = []
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        for i, line in enumerate(f, 1):
            if start_line <= i < end_line:
                lines.append(line.rstrip())
            if i >= end_line:
                break

    return '\n'.join(lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze-book.py <file_path> [command]")
        print("Commands:")
        print("  info      - Show basic book information")
        print("  chapters  - List all chapters")
        print("  extract <start> <end> - Extract a specified line range")
        sys.exit(1)

    file_path = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else 'info'

    if not os.path.exists(file_path):
        print(f"Error: File not found - {file_path}")
        sys.exit(1)

    encoding = detect_encoding(file_path)

    if command == 'info':
        info = get_book_info(file_path, encoding)
        chapters = find_chapters(file_path, encoding)

        print(f"Title: {info['title']}")
        print(f"File: {info['filename']}")
        print(f"Encoding: {encoding}")
        print(f"Total lines: {info['total_lines']}")
        print(f"Chapters: {len(chapters)}")
        print("\n=== Beginning of File ===")
        for line in info['first_lines'][:10]:
            if line:
                print(line)

    elif command == 'chapters':
        chapters = find_chapters(file_path, encoding)

        if not chapters:
            print("No chapter structure detected.")
            sys.exit(0)

        print(f"Found {len(chapters)} chapters:\n")
        for i, ch in enumerate(chapters, 1):
            print(f"{i:3d}. [line {ch['line']:5d}] {ch['title']}")

    elif command == 'extract':
        if len(sys.argv) < 5:
            print("Usage: python analyze-book.py <file_path> extract <start_line> <end_line>")
            sys.exit(1)

        start = int(sys.argv[3])
        end = int(sys.argv[4])
        content = extract_chapter_content(file_path, start, end, encoding)
        print(content)

if __name__ == '__main__':
    main()
