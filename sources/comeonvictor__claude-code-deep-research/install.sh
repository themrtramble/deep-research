#!/bin/bash
# Deep Research Skill installer for Claude Code
set -e

SKILL_DIR=".claude/skills/deep-research"

if [ ! -d ".claude" ] && [ ! -f "CLAUDE.md" ]; then
  echo "Warning: No .claude directory or CLAUDE.md found."
  echo "Make sure you're running this from your project root."
  read -p "Continue anyway? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

if [ -d "$SKILL_DIR" ]; then
  echo "deep-research skill already exists at $SKILL_DIR"
  read -p "Overwrite? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
  rm -rf "$SKILL_DIR"
fi

TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo "Downloading deep-research skill..."
git clone --quiet https://github.com/comeonvictor/claude-code-deep-research.git "$TEMP_DIR"

mkdir -p "$SKILL_DIR"
cp "$TEMP_DIR/SKILL.md" "$SKILL_DIR/"
cp -r "$TEMP_DIR/references" "$SKILL_DIR/"

echo ""
echo "Installed deep-research skill to $SKILL_DIR"
echo ""
echo "Usage: /deep-research [topic]"
echo ""
