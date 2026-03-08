#!/usr/bin/env bash
# install.sh — Install the book-summary skill for Soloent

set -e

SKILL_NAME="book-summary"
SKILL_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.soloent/skills/${SKILL_NAME}"

# ── Colors ────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ── Helpers ───────────────────────────────────────────────────────────────────
info()    { echo -e "${GREEN}✔${NC}  $1"; }
warn()    { echo -e "${YELLOW}⚠${NC}  $1"; }
error()   { echo -e "${RED}✘${NC}  $1"; exit 1; }

# ── Check dependencies ────────────────────────────────────────────────────────
echo ""
echo "  book-summary skill installer"
echo "  ─────────────────────────────"
echo ""

if ! command -v python3 &>/dev/null; then
  error "python3 is required but not installed. Install it from https://python.org and try again."
fi
info "python3 found: $(python3 --version)"

# ── Choose install target ─────────────────────────────────────────────────────
echo ""
echo "  Where would you like to install the skill?"
echo "  [1] Global  — ~/.soloent/skills/  (available in all projects)"
echo "  [2] Project — .soloent/skills/    (current directory only)"
echo ""
read -rp "  Enter 1 or 2 [default: 1]: " choice
choice="${choice:-1}"

if [[ "$choice" == "2" ]]; then
  DEST_DIR="$(pwd)/.soloent/skills/${SKILL_NAME}"
  INSTALL_TYPE="project"
else
  DEST_DIR="${HOME}/.soloent/skills/${SKILL_NAME}"
  INSTALL_TYPE="global"
fi

# ── Install ───────────────────────────────────────────────────────────────────
echo ""

if [[ -d "$DEST_DIR" ]]; then
  warn "Skill already exists at: ${DEST_DIR}"
  read -rp "  Overwrite? [y/N]: " overwrite
  if [[ "${overwrite,,}" != "y" ]]; then
    echo "  Aborted."
    exit 0
  fi
  rm -rf "$DEST_DIR"
fi

mkdir -p "$DEST_DIR"
cp -r "${SKILL_SRC}/." "$DEST_DIR"

info "Installed to: ${DEST_DIR}  (${INSTALL_TYPE})"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "  ✅  book-summary skill is ready."
echo ""
echo "  Usage in Soloent:"
echo "    /book-summary /path/to/book.txt"
echo "    /book-summary /path/to/book.md"
echo ""
