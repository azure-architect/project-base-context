#!/bin/bash

# Workflow Documentation Transfer Script
# Transfers new IADPVEC workflow procedures from microservices-01 to project-base-context
# Creates necessary directories and copies workflow files only

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Source and target directories
SOURCE_DIR="/Volumes/Samsung/mo/projects/research/proof-of-concepts/sandbox/microservices-01"
TARGET_DIR="/Volumes/Samsung/mo/projects/research/proof-of-concepts/sandbox/project-base-context"

echo -e "${BLUE}=== Workflow Documentation Transfer ===${NC}"
echo -e "${BLUE}Transferring IADPVEC workflow procedures to base context repository${NC}"
echo

# Change to target directory
cd "$TARGET_DIR"

echo -e "${YELLOW}Step 1: Creating required directories...${NC}"

# Create necessary directories for timestamped file systems
mkdir -p project_status
mkdir -p commit_statements

# Add .gitkeep files to empty directories (so they get tracked in git)
touch project_status/.gitkeep
touch commit_statements/.gitkeep

echo -e "${GREEN}✅ Created project_status/ and commit_statements/ directories${NC}"

echo -e "${YELLOW}Step 2: Copying workflow documentation files...${NC}"

# Copy new workflow procedures
cp "$SOURCE_DIR/workflows/iadpvec_task_proposal.md" workflows/
cp "$SOURCE_DIR/workflows/iadpvec_task_validation.md" workflows/
cp "$SOURCE_DIR/workflows/project_status_update.md" workflows/
cp "$SOURCE_DIR/workflows/git_commit_with_prepared_message.md" workflows/

echo -e "${GREEN}✅ Copied 4 workflow documentation files${NC}"

echo -e "${YELLOW}Step 3: Copying framework documentation...${NC}"

# Copy enhanced documentation
cp "$SOURCE_DIR/COMPLETION_SUMMARY.md" docs/
cp "$SOURCE_DIR/VIOLATIONS.md" docs/

echo -e "${GREEN}✅ Copied 2 documentation files to docs/${NC}"

echo -e "${YELLOW}Step 4: Verification...${NC}"

# Verify files were copied successfully
echo "Checking copied files:"
echo "- workflows/iadpvec_task_proposal.md: $([ -f workflows/iadpvec_task_proposal.md ] && echo "✅" || echo "❌")"
echo "- workflows/iadpvec_task_validation.md: $([ -f workflows/iadpvec_task_validation.md ] && echo "✅" || echo "❌")"
echo "- workflows/project_status_update.md: $([ -f workflows/project_status_update.md ] && echo "✅" || echo "❌")"
echo "- workflows/git_commit_with_prepared_message.md: $([ -f workflows/git_commit_with_prepared_message.md ] && echo "✅" || echo "❌")"
echo "- docs/COMPLETION_SUMMARY.md: $([ -f docs/COMPLETION_SUMMARY.md ] && echo "✅" || echo "❌")"
echo "- docs/VIOLATIONS.md: $([ -f docs/VIOLATIONS.md ] && echo "✅" || echo "❌")"

echo
echo -e "${BLUE}=== Transfer Complete ===${NC}"
echo -e "${GREEN}Enhanced IADPVEC workflow procedures are now available in project-base-context${NC}"
echo -e "${GREEN}Ready to commit using target repository's git procedures${NC}"
echo
echo "Next steps:"
echo "1. Review transferred files"
echo "2. Use scripts/git-commit-update.sh to commit changes"
echo "3. New projects can now use enhanced workflow procedures"
