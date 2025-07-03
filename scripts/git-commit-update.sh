#!/bin/bash
# scripts/git-commit-update.sh - Commit changes and update project status
# Part of the Context Engineering + IADPVEVC framework

set -e

# Force git to not use editor for commits
export GIT_EDITOR=:
export EDITOR=:
export VISUAL=:

if [ $# -eq 0 ]; then
    echo "❌ Usage: scripts/git-commit-update.sh 'commit message' ['status message']"
    echo "📝 Examples:"
    echo "   scripts/git-commit-update.sh 'Complete Docker infrastructure setup'"
    echo "   scripts/git-commit-update.sh 'Fix port mappings' 'Infrastructure ready for testing'"
    exit 1
fi

COMMIT_MSG="$1"
STATUS_MSG="${2:-Ready for next development phase}"  # Default status if not provided

# Verify we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Must be run from project root (no .git directory found)"
    exit 1
fi

# Check if there are changes to commit
if git diff --staged --quiet && git diff --quiet; then
    echo "⚠️  No changes to commit. Use 'git add .' first if you have unstaged changes."
    echo "🔄 Updating status only..."
    
    # Just update status without committing
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
    
    echo "✅ Status updated (no commit made)"
    exit 0
fi

# Stage all changes
git add .

# Show what will be committed (without pager)
echo "📋 Changes to be committed:"
git --no-pager diff --staged --name-status

# Commit the changes with aggressive no-editor settings
echo "📋 Committing with message: $COMMIT_MSG"
git -c core.editor=true -c sequence.editor=true commit -m "$COMMIT_MSG" --no-edit --quiet

# Create comprehensive status summary file
echo "=== PROJECT SUMMARY ===" > .git/PROJECT_STATUS.txt
echo "Last updated: $(date)" >> .git/PROJECT_STATUS.txt
echo "Last commit: $COMMIT_MSG" >> .git/PROJECT_STATUS.txt
echo "" >> .git/PROJECT_STATUS.txt

echo "RECENT COMMITS:" >> .git/PROJECT_STATUS.txt
git log --oneline -5 >> .git/PROJECT_STATUS.txt
echo "" >> .git/PROJECT_STATUS.txt

echo "CURRENT STATUS:" >> .git/PROJECT_STATUS.txt
echo "$STATUS_MSG" >> .git/PROJECT_STATUS.txt
echo "" >> .git/PROJECT_STATUS.txt

echo "BRANCH INFO:" >> .git/PROJECT_STATUS.txt
echo "Current branch: $(git branch --show-current)" >> .git/PROJECT_STATUS.txt
echo "Repository status: $(git status --porcelain | wc -l | tr -d ' ') uncommitted files" >> .git/PROJECT_STATUS.txt

echo "✅ Committed: $COMMIT_MSG"
echo "📄 Status: $STATUS_MSG"
echo "📁 Summary available in .git/PROJECT_STATUS.txt"
