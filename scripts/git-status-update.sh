#!/bin/bash
# scripts/git-status-update.sh - Update project status without committing
# Part of the Context Engineering + IADPVEC framework

set -e

if [ $# -eq 0 ]; then
    echo "❌ Usage: scripts/git-status-update.sh 'status message'"
    echo "📝 Example: scripts/git-status-update.sh 'Discussed Docker testing approach, proceeding with validation'"
    exit 1
fi

STATUS_MSG="$1"

# Verify we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Must be run from project root (no .git directory found)"
    exit 1
fi

# Create/update status file
echo "=== PROJECT STATUS UPDATE ===" > .git/PROJECT_STATUS.txt
echo "Updated: $(date)" >> .git/PROJECT_STATUS.txt
echo "" >> .git/PROJECT_STATUS.txt

echo "RECENT COMMITS:" >> .git/PROJECT_STATUS.txt
git log --oneline -5 >> .git/PROJECT_STATUS.txt
echo "" >> .git/PROJECT_STATUS.txt

echo "CURRENT STATUS:" >> .git/PROJECT_STATUS.txt
echo "$STATUS_MSG" >> .git/PROJECT_STATUS.txt
echo "" >> .git/PROJECT_STATUS.txt

echo "BRANCH INFO:" >> .git/PROJECT_STATUS.txt
echo "Current branch: $(git branch --show-current)" >> .git/PROJECT_STATUS.txt
echo "Last commit: $(git log -1 --pretty=format:'%h - %s (%cr)')" >> .git/PROJECT_STATUS.txt

echo "✅ Project status updated in .git/PROJECT_STATUS.txt"
echo "📄 Status: $STATUS_MSG"
