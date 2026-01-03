# ⛓️ ChainCredit - Resume-Based Git Repository Skill Analyzer

AI-powered resume analysis tool that verifies developer skills by analyzing their actual GitHub contributions. Uses Gemini API to parse resumes and extract GitHub repositories, then performs deep code analysis to validate claimed skills.

> **🔍 Code Audit Completed:** January 3, 2026  
> **🤖 AI-Powered Resume Parser:** Gemini API Integration  
> See [AUDIT_REPORT.md](AUDIT_REPORT.md) for comprehensive fixes to scoring logic, bot detection, and validation.

## 🚀 What's New

**Resume-First Approach:**
- Upload your resume (PDF/DOCX) instead of manual repo URLs
- AI extracts skills and GitHub projects automatically
- Verifies resume skills against actual code contributions
- Generates comprehensive skill assessment report

## 📁 Project Structure

```
ChainCredit/
├── main.py                    # Entry point - resume-based analyzer
├── resume_parser.py           # Gemini API resume parsing
├── display_resume.py          # Resume-specific result display
├── config.py                  # Configuration constants & parameters
├── repo_manager.py            # Repository cloning & cleanup
├── analyzer.py                # Repository analysis orchestration
├── scoring.py                 # General skill scoring calculations
├── skill_scorer.py            # Technology-specific skill evaluation
├── display.py                 # Output formatting & display
├── utils.py                   # Validation, bot detection, warnings
├── tests.py                   # Test case documentation
├── AUDIT_REPORT.md            # Comprehensive audit & fix documentation
│
└── code_analysis/             # Code analysis modules
    ├── __init__.py
    ├── language_detector.py   # Language & framework detection
    ├── structure.py           # Folder & architecture analysis
    ├── complexity.py          # Cyclomatic complexity metrics
    ├── lint_metrics.py        # Style & code quality conventions
    └── test_detector.py       # Test coverage & framework detection
```

## 🚀 Features

### General Skill Scoring`(author_lines / total_lines) × 100` - consistent everywhere
- **Commit Maturity (20%)**: Commit patterns, complexity trends
- **Project Complexity (10%)**: File coverage, tech diversity

### Validation & Quality
- ✅ **Score Validation**: All scores strictly ∈ [0, 100]
- ✅ **Bot Detection**: Automatically excludes dependabot, github-actions, etc.
- ✅ **Consistent Authorship**: Single formula used across all skill evaluations
- ✅ **Zero-Score Handling**: Explicitly shows undetected skills with reasons
- ✅ **Warnings & Assumptions**: Logs limitations and assumptions automaticalldiversity
- **Authorship Confidence (25%)**: Commit frequency, contribution volume
- **Commit Maturity (20%)**: Commit patterns, complexity trends
- **Project Complexity (10%)**: File coverage, tech diversity

### Technology-Specific Skills
Rule-based evaluation for:

**Frameworks:**
- **React**: Component usage, hooks, project size, maturity
- **Django**: App structure, ORM usage, REST API patterns
- **Node.js**: API design, middleware, routing patterns
- **TailwindCSS**: Utility classes, config customization, project scale

**Programming Languages:**
- **Python**: File presence, project structure, function complexity, git maturity
- **JavaScript**: Modern JS syntax, modularity, code patterns
- **TypeScript**: Type safety, tsconfig, type annotations
- **C**: Pointer usage, memory management, modular design
- **C++**: OOP patterns, memory management, class structure

### Code Analysis
- **Language Detection**: Identifies programming languages by file extensions and LOC
- **Framework Detection**: Detects React, Django, Flask, Node.js, Vue, Angular, etc.
- **Structural Analysis**: MVC patterns, microservices, layered architecture
- **Complexity Metrics**: Lines of code, functions, classes, cyclomatic complexity
- **Quality Indicators**: Linter configs, formatters, type checking, documentation
- **Test Detection**: Identifies test frameworks (pytest, jest, mocha, etc.)

## 🎯 Use Cases

### For Job Seekers
- **Resume Validation**: Verify that your resume accurately reflects your GitHub contributions
- **Skill Assessment**: Get objective metrics on your technology proficiency
- **Portfolio Enhancement**: Identify gaps between claimed and demonstrated skills

### For Recruiters
- **Quick Screening**: Automatically analyze candidates from their resumes
- **Skill Verification**: Confirm candidate claims with actual code analysis
- **Fair Comparison**: Objective metrics across all candidates

### For Hiring Managers
- **Technical Assessment**: Understand candidate's real-world coding experience
- **Project Quality**: Evaluate code quality and contribution patterns
- **Team Fit**: See technologies they've actually worked with

## � Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[AUDIT_REPORT.md](AUDIT_REPORT.md)** - Comprehensive code audit & fixes
- **[EXAMPLES.md](EXAMPLES.md)** - Sample outputs and use cases
- **[sample_resume_template.txt](sample_resume_template.txt)** - Resume template

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Add more programming language evaluators
- Enhance framework detection patterns
- Improve bot detection algorithms
- Support for private repositories
- Resume parsing improvements

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- **Gemini API**: https://makersuite.google.com/app/apikey
- **GitPython Docs**: https://gitpython.readthedocs.io/
- **PyDriller Docs**: https://pydriller.readthedocs.io/

---

**Made with ⛓️ by ChainCredit** | Resume-First Developer Skill Verification

Edit [config.py](config.py) to customize:
- Scoring weights
- Skill level thresholds
- Framework detection patterns
- Complexity metrics

## ⚠️ Requirements

### System Requirements
- Python 3.10+
- Git installed and accessible
- Internet connection for GitHub access

### API Requirements
- **Gemini API Key** (required for resume parsing)
- Get free key at: https://makersuite.google.com/app/apikey

### Resume Requirements
Your resume must include:
- ✅ GitHub repository URLs
- ✅ Technical skills list
- ✅ Name and contact info
- ✅ PDF or DOCX format

## 🧪 Testing

```bash
# Test with sample resume
python main.py samples/sample_resume.pdf

# Expected: Extracts skills and repos, analyzes contributions
```

## 🎯 Supported Technologies

### Frameworks (100-point scale each)
- ✅ **React** - Component patterns, hooks, modern React
- ✅ **Django** - App structure, ORM, REST APIs
- ✅ **Node.js** - Express/Fastify/Koa, middleware, routing
- ✅ **TailwindCSS** - Utility classes, configuration

### Programming Languages (100-point scale each)
- ✅ **Python** - Project structure, complexity, git maturity
- ✅ **JavaScript** - Modern ES6+, modularity, patterns
- ✅ **TypeScript** - Type safety, strict typing, config
- ✅ **C** - Memory management, pointers, modular design

## 🔍 How It Works

### 1. Resume Parsing (Gemini AI)
```python
# Extract from PDF/DOCX
resume_data = parse_resume_file('resume.pdf')

# Returns:
{
  'candidate_name': 'John Doe',
  'email': 'john@example.com',
  'github_username': 'johndoe',
  'skills': ['Python', 'React', 'Django'],
  'github_repos': ['https://github.com/johndoe/project1', ...]
}
```

### 2. Repository Analysis
For each GitHub repo in resume:
- Clone repository
- Analyze commits by the candidate only
- Calculate skill scores
- Evaluate technology-specific proficiency

### 3. Skill Verification
- **Verified**: Skills from resume found in code
- **Not Verified**: Resume skills with no evidence
- **Additional**: Skills detected but not in resume

## 📊 Scoring Methodology

### General Skill Score Formula
3. **Project Size** (20 pts): Lines of code thresholds
4. **Git Maturity** (20 pts): Commit count
5. **Authorship Confidence** (20 pts): Code ownership ratio

#### Django Evaluation
1. **Django Presence** (20 pts): Django in requirements.txt
2. **App Structure** (20 pts): Number of Django apps
3. **ORM Usage** (20 pts): Model patterns detected
4. **REST Practices** (20 pts): API view patterns
5. **Authorship Confidence** (20 pts): Code ownership

#### Node.js Evaluation
1. **Node Presence** (20 pts): Express/Fastify/Koa detection
2. **API Design** (20 pts): Route definitions
3. **Middleware Usage** (20 pts): Middleware patterns
4. **Git Maturity** (20 pts): Commit history
5. **Authorship Confidence** (20 pts): Ownership

#### TailwindCSS Evaluation
1. **Tailwind Presence** (20 pts): Package dependency detection
2. **Utility Usage** (20 pts): Utility class patterns
3. **Config Customization** (20 pts): tailwind.config.js presence
4. **Project Scale** (20 pts): Lines of code with Tailwind
5. **Authorship Confidence** (20 pts): Code ownership

### Language Evaluations

#### Python Evaluation
1. **Python Presence** (20 pts): Number of .py files (1/5/10+)
2. **Python Structure** (20 pts): setup.py, __init__.py, pyproject.toml
3. **Function Complexity** (20 pts): Average function length (<40/70 lines)
4. **Git Maturity** (20 pts): Commit count (5/12/25+)
5. **Authorship Confidence** (20 pts): Code ownership ratio

#### JavaScript Evaluation
1. **JS Presence** (20 pts): Number of .js files (3/8/15+)
2. **Modern JS Usage** (20 pts): Arrow functions, async/await, ES6 imports
3. **Modularity** (20 pts): File organization (10/20+ files)
4. **Git Maturity** (20 pts): Commit count (6/15/30+)
5. **Authorship Confidence** (20 pts): Code ownership

#### TypeScript Evaluation
1. **TS Presence** (20 pts): Number of .ts/.tsx files (1/5/10+)
2. **Type Safety** (20 pts): Type annotations, interfaces, types
3. **Config Quality** (20 pts): tsconfig.json presence
4. **Git Maturity** (20 pts): Commit count (5/12/25+)
5. **Authorship Confidence** (20 pts): Code ownership

#### C Evaluation
1. **C Presence** (20 pts): Number of .c/.h files (1/5/10+)
2. **Pointer Usage** (20 pts): malloc, free, pointer operations
3. **Modular Design** (20 pts): Header/source file pairs (3/5+)
4. **Git Maturity** (20 pts): Commit count (4/10/20+)
5. **Authorship Confidence** (20 pts): Code ownership

#### C++ Evaluation
1. **C++ Presence** (20 pts): Number of .cpp/.hpp files (1/5/10+)
2. **OOP Usage** (20 pts): Classes, public/private, inheritance
3. **Memory Management** (20 pts): Smart pointers, new/delete
4. **Git Maturity** (20 pts): Commit count (5/12/25+)
5. **Authorship Confidence** (20 pts): Code o patterns
5. **Authorship Confidence** (20 pts): Code ownership

### Node.js Evaluation
1. **Node Presence** (20 pts): Express/Fastify/Koa detection
2. **API Design** (20 pts): Route definitions
3. **Middleware Usage** (20 pts): Middleware patterns
4. **Git Maturity** (20 pts): Commit history
5. **Authorship Confidence** (20 pts): Ownership

## 🛠️ Installation

```bash
# Clone repository
git clone <repo-url>
cd ChainCredit

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install GitPython pydriller numpy tqdm PyPDF2 python-docx google-genai python-dotenv

# Set up Gemini API key
cp .env.example .env
# Edit .env and add your API key
```

### Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy `.env.example` to `.env`
4. Add your key: `GEMINI_API_KEY='your-key-here'`

## 📖 Usage

### Resume-Based Analysis (Recommended)

```bash
# Analyze from resume
python main.py resume.pdf

# Or with DOCX
python main.py resume.docx
```

**Your resume should include:**
- Full name
- Email address (optional)
- GitHub username or profile URL
- List of technical skills
- **GitHub repository URLs** of your projects

### Example Resume Format

```
John Doe
Email: john@example.com
GitHub: github.com/johndoe

SKILLS:
Python, JavaScript, React, Django, Node.js, TailwindCSS

PROJECTS:
- E-commerce Platform: https://github.com/johndoe/ecommerce-app
- Task Manager: https://github.com/johndoe/task-manager
- Portfolio Website: https://github.com/johndoe/portfolio
```

## 📈 Output

The analyzer provides:

1. **Repository Overview**
   - Commit count, contributors, files, LOC
   - Functions, classes, complexity metrics

2. **Technology Stack**
   - Detected languages with LOC distribution
   - Frameworks with confidence levels
   - Test frameworks and coverage
riteria breakdown
   - Shows 0/100 for undetected skills with explanations
   
5. **Bot Detection**
   - Automated contributors shown separately
   - Excluded from skill scoring
   
6. **Warnings & Assumptions**
   - Logs detected limitations
   - Documents scoring assumptions
3. **General Skill Score**
   - Overall skill level (Beginner/Intermediate/Advanced/Expert)
   - Breakdown by scoring criteria

4. **Technology-Specific Skills**
   - Per-framework skill scores (0-100)
   - Detailed cframeworks (Vue, Angular, Spring, Flask, FastAPI)
- [ ] Add more languages (Java, Go, Rust, Ruby, PHP)
- [ ] Implement AI-powered code review
- [ ] Add blockchain credential verification
- [ ] Export results to JSON/PDF
- [ ] Web dashboard with charts
- [ ] Multi-repository batch analysis
- [ ] GitHub/GitLab API integration
- [ ] Real-time repository monitoring
- [ ] Team collaboration analytics
- Threshold values for criteria
- Skill level boundaries

## 🧪 Code Analysis Modules

### `language_detector.py`
- Scans repository for programming languages
- Detects frameworks via package files and code patterns
- Returns confidence scores for each technology

### `structure.py`
- Analyzes folder organization
- Detects architectural patterns (MVC, microservices, layered)
- Counts Django apps and modular components

### `complexity.py`
- Calculates lines of code (total, code, comments, blank)
- Counts functions and classes
- Measures average function length

### `lint_metrics.py`
- Checks for linter/formatter configs
- Calculates documentation ratio
- Analyzes naming conventions

### `test_detector.py`
- Identifies test files and frameworks
- Estimates test coverage
- Detects pytest, jest, mocha, unittest, etc.

## 🎓 Skill Levels

- **🌟 Expert**: Score ≥ 70
- **⭐ Advanced**: Score ≥ 50
- **💫 Intermediate**: Score ≥ 30
- **✨ Beginner**: Score < 30

## 🔮 Future Enhancements

- [ ] Add more technologies (Vue, Angular, Spring, etc.)
- [ ] Implement AI-powered code review
- [ ] Add blockchain credential verification
- [ ] Export results to JSON/PDF
- [ ] Web dashboard
- [ ] Multi-repository batch analysis
- [ ] GitHub/GitLab API integration

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! To add a new technology:

1. Update `language_detector.py` with detection patterns
2. Add scoring criteria to `skill_scorer.py`
3. Define thresholds in respective methods
4. Test with sample repositories

---

**Built with Python 🐍 | Powered by GitPython & PyDriller 🔧**
