### 🔄 Context Awareness & Project Understanding
- **Always read `PLANNING.md`** first to understand architecture, goals, and constraints
- **Check `TASK.md`** before starting work - add new tasks with date if missing
- **Review relevant examples** in the `examples/` folder for patterns to follow
- **Never assume missing context** - ask questions if uncertain about requirements
- **Follow IADPVEC methodology** - never jump straight to implementation

### 🚦 IADPVEC Execution Protocol
- **INGEST**: Analyze current state and gather all relevant context
- **ASSESS**: Evaluate what's working, broken, or needed using available documentation
- **DISCUSS**: Present findings and proposed solutions clearly
- **PLAN**: Create detailed, step-by-step implementation plan
- **VALIDATE**: Confirm implementation meets requirements before proceeding
- **EXECUTE**: Implement only after explicit developer approval
- **COMMIT**: Document changes in git with comprehensive commit messages

### 🧱 Code Structure & Architecture
- **Never create files longer than 500 lines** - refactor into modules
- **Follow consistent patterns** from `examples/` and `PLANNING.md`
- **Organize by feature/responsibility**:
  - `agent.py` - Main agent definition and logic
  - `tools.py` - Tool functions and integrations
  - `models.py` - Data models and validation
  - `config.py` - Configuration and settings
- **Use relative imports** within packages for cleaner dependencies

### 🧪 Testing & Quality Assurance
- **Create comprehensive tests** for all new features using patterns from `examples/testing/`
- **Mirror main structure** in `/tests` folder
- **Include minimum test cases**:
  - Expected use case
  - Edge case handling
  - Failure scenario
- **Update existing tests** when modifying logic
- **Ensure 80%+ test coverage** for critical components

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them
- **Add new sub-tasks or TODOs** discovered during development to `TASK.md` under "Discovered During Work" section
- **Reference task completion** in commit messages for traceability

### 📎 Style & Standards
- **Language**: Python as primary language
- **Formatting**: PEP8 compliance, type hints, Black formatting
- **Validation**: Pydantic for data validation
- **APIs**: FastAPI with SQLAlchemy/SQLModel for persistence
- **Documentation**: Google-style docstrings for all functions
- **Environment**: python_dotenv with .env configuration

### 📚 Documentation & Knowledge Preservation
- **Update README.md** when adding features or changing setup
- **Comment complex logic** with `# Reason:` explanations
- **Create comprehensive commit messages** that serve as breadcrumbs
- **Generate PRPs** for complex features using `/generate-prp`
- **Maintain examples** that demonstrate current best practices

### 🔒 Security & Safety Rules
- **Never commit secrets** - use .env files with .gitignore
- **Validate all inputs** using Pydantic models
- **Handle errors gracefully** with proper exception handling
- **Never hallucinate dependencies** - only use verified packages
- **Confirm file paths exist** before referencing in code

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.
- **Always wait for explicit permission** before executing implementations (never assume approval)

### 🎯 Success Criteria
- **All tests pass**: `pytest tests/ -v`
- **Code quality**: `ruff check .` and `mypy .` with no errors
- **Functionality works**: Manual testing confirms requirements met
- **Documentation complete**: README and relevant docs updated
- **Git history clean**: Meaningful commits with clear progression

### 🔄 Process Integration
- **Context Engineering**: Use comprehensive examples and documentation for understanding
- **IADPVEC Workflow**: Follow structured approach for all implementations
- **Quality Gates**: Meet all technical and process requirements before completion
- **Knowledge Sharing**: Contribute back to examples and documentation based on learnings