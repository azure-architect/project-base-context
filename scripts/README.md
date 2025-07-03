# Git Workflow Scripts

Scripts for managing git commits and project status in the Context Engineering + IADPVEC framework.

## 📋 Available Scripts

### **git-status-update.sh** - Status Update Only
Updates project status without making a commit.

**Usage:**
```bash
scripts/git-status-update.sh "status message"
```

**Example:**
```bash
scripts/git-status-update.sh "Discussed Docker testing approach, proceeding with infrastructure validation"
```

### **git-commit-update.sh** - Commit + Status Update  
Commits changes and updates project status.

**Usage:**
```bash
scripts/git-commit-update.sh "commit message" ["optional status message"]
```

**Examples:**
```bash
# Commit with default status
scripts/git-commit-update.sh "Complete Docker infrastructure setup"

# Commit with custom status
scripts/git-commit-update.sh "Fix port mapping strategy" "Infrastructure ready for docker-compose testing"
```

## 🚀 Setup Instructions

### **1. Make Scripts Executable**
```bash
chmod +x scripts/git-status-update.sh
chmod +x scripts/git-commit-update.sh
```

### **2. Create Aliases in .zshrc**
Add these lines to your `~/.zshrc`:

```bash
# Git workflow aliases for Context Engineering framework
alias gsu='scripts/git-status-update.sh'      # Status update only
alias gcu='scripts/git-commit-update.sh'      # Commit + status update
```

Then reload: `source ~/.zshrc`

### **3. Text Expansion Setup**
Create text expansions that trigger these commands:

**For Status Updates:**
- **Trigger:** `;;gsu`
- **Expansion:** `scripts/git-status-update.sh "REPLACE_WITH_MESSAGE"`

**For Commits:**
- **Trigger:** `;;gcu` 
- **Expansion:** `scripts/git-commit-update.sh "REPLACE_WITH_MESSAGE"`

**For Commits with Status:**
- **Trigger:** `;;gcus`
- **Expansion:** `scripts/git-commit-update.sh "REPLACE_WITH_COMMIT" "REPLACE_WITH_STATUS"`

## 📄 Output File

Both scripts create/update `.git/PROJECT_STATUS.txt` with:
- **Timestamp** of last update
- **Recent commits** (last 5)
- **Current status** message
- **Branch information**
- **Repository status**

## 🔄 AI Assistant Integration

When an AI assistant (like Claude) needs to get up to speed with a project:

1. **Read `.git/PROJECT_STATUS.txt`** for complete current context
2. **Understand recent work** from commit history
3. **Know current status** and next steps
4. **Have recovery information** for interrupted sessions

## 💡 Usage Tips

### **During Development Sessions:**
- **Status updates** for discussions and planning: `gsu "message"`
- **Commits** for completed work: `gcu "what was done" "current status"`

### **For IADPVEC Workflow:**
- **After DISCUSS phase:** Status update with agreed approach
- **After EXECUTE phase:** Commit with what was implemented
- **Session interruptions:** Status update with current phase

### **Best Practices:**
- **Be descriptive** in status messages for future recovery
- **Include next steps** in status for continuity
- **Reference IADPVEC phases** when relevant
- **Update regularly** during long development sessions

## 🎯 Framework Integration

These scripts are designed to work with the Context Engineering + IADPVEC methodology:

- **Context preservation** through detailed status tracking
- **Recovery support** for interrupted sessions  
- **IADPVEC compliance** by documenting workflow phases
- **Knowledge breadcrumbs** for future development

---

**Part of the Context Engineering + IADPVEC unified framework for reliable AI-assisted development.**
