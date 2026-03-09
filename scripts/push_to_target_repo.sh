#!/usr/bin/env bash
set -euo pipefail

TARGET_REMOTE="git@github.com:ListenToATree/docs.git"

cd "$(dirname "$0")/.."

if [ ! -d .git ]; then
  git init
  git branch -M main
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "$TARGET_REMOTE"
fi

git add .
if ! git diff --cached --quiet; then
  git commit -m "docs: update product and tech refactor documentation"
fi

git push -u origin main

echo "Pushed docs to $TARGET_REMOTE"
