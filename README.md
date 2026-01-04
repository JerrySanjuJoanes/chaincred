# ⛓️ ChainCredit - Resume Skill Verification System

**Automatically verify developer skills by analyzing their GitHub contributions.**

ChainCredit is a resume verification tool that reads your PDF resume, extracts claimed technical skills and GitHub repository URLs, then analyzes your actual code contributions to verify each skill. It separates what you claim from what you can actually prove through code.

> **🎯 What It Does:**  
> 1. Reads your resume PDF to extract skills and GitHub URLs  
> 2. Analyzes your commits and code in each repository  
> 3. Scores each skill (0-100) based on actual usage and contribution level  
> 4. Separates **Verified Skills** (found in your code) from **Unverified Skills** (claimed but not detected)

## 🚀 Key Features

- ✅ **GitHub URL Validation** - Skips profile URLs, only analyzes repository URLs
- ✅ **Claimed vs Verified** - Clearly separates resume claims from code evidence
- ✅ **Per-Skill Scoring** - Individual scores for React, Django, Python, JavaScript, etc.
- ✅ **Contribution-Weighted** - Your score depends on how much code YOU wrote
- ✅ **Multi-Repository Aggregation** - Combines scores across all your projects
- ✅ **Evidence-Based** - Shows specific files, imports, and patterns detected
- ✅ **AI + Regex Fallback** - Uses Gemini API with regex backup for resume parsing

## 📁 Project Structure

```
ChainCredit/
├── main.py                          # Entry point (delegates to cli/)
│
├── cli/                             # Command-line interface
│   ├── main.py                      # 3-stage orchestrator (Resume → Repos → Report)
│   ├── display.py                   # Header display
│   └── display_resume.py            # Resume-focused reporting
│
├── resume/                          # Resume parsing
│   ├── resume_parser.py             # Gemini API + regex extraction
│   └── create_resume_pdf.py         # Test resume generator (unused)
│
├── repos/                           # Repository management
│   ├── repo_manager.py              # Clone & cleanup
│   └── analyzer.py                  # Repository analysis
│
├── scoring/                         # Skill scoring system
│   ├── skill_scorer.py              # 5-criterion heuristic scoring
│   ├── skill_detector.py            # Evidence collection (files/imports)
│   ├── contribution_scorer.py       # Contribution-based capping
│   └── heuristics_adapter.py        # Bridges heuristics into scoring flow
│
├── shared/                          # Shared utilities
│   ├── config.py                    # Configuration constants
│   └── utils.py                     # Validation & bot detection
│
└── code_analysis/                   # Code metrics
    ├── language_detector.py         # Language & framework detection
    ├── structure.py                 # Architecture analysis
    ├── complexity.py                # LOC & complexity metrics
    ├── lint_metrics.py              # Code quality checks
    └── test_detector.py             # Test framework detection
```

## 🎯 How It Works

**3-Stage Process:**

### Stage 1: Resume Parsing
- Extracts your name, email, skills, and GitHub URLs from PDF
- Uses Gemini API (AI) with regex fallback
- Validates URLs (skips profile links, keeps only repository URLs)

### Stage 2: Repository Analysis
For each GitHub repository:
- Clones the repository locally
- Analyzes your commits and code contributions
- Detects technologies from file extensions and imports
- Calculates contribution percentage (your lines / total lines)

### Stage 3: Skill Scoring & Reporting
- **Heuristic Scoring**: 5 criteria per skill (20 points each = 100 total)
  - Presence detection (dependencies/imports)
  - Feature usage (React hooks, Django ORM, etc.)
  - Project size (lines of code)
  - Git maturity (commit count)
  - Authorship confidence (contribution %)
  
- **Contribution Caps**: Your score is capped based on your contribution level
  - < 5% contribution: Insufficient (0 points)
  - < 10% contribution: Max 40 points
  - < 30% contribution: Max 60 points
  - ≥ 70% contribution: Full score (100 points possible)

- **Multi-Repo Aggregation**: Weighted average across all repositories

## 📊 Output Categories

**1. Verified Skills (Resume + Code Evidence)**
- Skills you claimed AND were detected in your code
- Shows score (0-100), evidence, and repository breakdown

**2. Unverified Skills (Resume Only)**
- Skills you claimed but NOT detected in your code
- Shows 0/100 with explanation

**For Job Seekers:**
- Verify your resume is backed by real code
- Get objective skill scores for your portfolio
- Identify skill gaps to work on

**For Recruiters:**
- Quickly verify candidate claims
- Get objective skill comparisons
- Save hours on technical screening

**For Hiring Managers:**
- Understand real coding experience
- See actual project contributions
- Make data-driven hiring decisions
### For Hiring Managers
- **Technical Assessment**: Understand candidate's real-world coding experience
- **Project Quality**: Evaluate code quality and contribution patterns
- **Team Fit**: See technologies they've actually worked with

## � Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[AUDIT_REPORT.md](AUDIT_REPORT.md)** - Comprehensive code audit & fixes
## 🛠️ Supported Technologies

**Frameworks (100-point heuristic scoring):**
- ✅ React - Component patterns, hooks, modern React
- ✅ Django - App structure, ORM, REST APIs
- ✅ Node.js - Express/Fastify/Koa, middleware, routing
- ✅ TailwindCSS - Utility classes, configuration

**Programming Languages (100-point heuristic scoring):**
- ✅ Python - Project structure, complexity, git maturity
- ✅ JavaScript - Modern ES6+, modularity, patterns
- ✅ TypeScript - Type safety, strict typing, config
- ✅ C - Memory management, pointers, modular design
- ✅ C++ - OOP patterns, class structure

**Other Technologies (evidence-based detection):**
- HTML, CSS, SQL, PostgreSQL, MongoDB, Redis, Docker, Git, and more...

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

## 🛠️ Installation

**Requirements:**
- Python 3.10+
- Git installed
- Internet connection
- Gemini API key (free at https://makersuite.google.com/app/apikey)

**Setup:**

```bash
# Clone repository
git clone <your-repo-url>
cd ChainCredit

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install GitPython pydriller numpy tqdm PyPDF2 PyMuPDF python-docx google-genai python-dotenv

# Create .env file
echo 'GEMINI_API_KEY=your-key-here' > .env
```

**Get Gemini API Key:**
1. Visit https://makersuite.google.com/app/apikey
2. Create a free API key
3. Add to `.env` file
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
� Usage

```bash
# Activate virtual environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Run analysis
python main.py your_resume.pdf
```

**Resume Requirements:**
Your PDF resume must include:
- ✅ Technical skills (Python, React, Django, etc.)
- ✅ GitHub repository URLs (not profile URLs)
- ✅ Your name (optional but helpful)

**Example Resume Section:**
```
SKILLS: Python, React, Django, JavaScript, HTML, CSS

PROJECTS:
- E-commerce App: https://github.com/yourusername/ecommerce
- Task Manager: https://github.com/yourusername/taskmanager
```ip

### Language Evaluations

#### Python Evaluation
1. **Python Presence** (20 pts): Number of .py files (1/5/10+)
2. *� Example Output

```
🔍 SKILL VERIFICATION RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 VERIFIED SKILLS (Resume + Code Evidence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ React: 84/100 ⭐ Advanced
   📦 Repository Breakdown:
   ├─ ecommerce-app (100% contribution) → 84/100 🎯 High Confidence
   └─ Evidence: 15 .jsx files, React hooks detected, modern patterns

✅ Python: 72/100 ⭐ Advanced
   📦 Repository Breakdown:
   ├─ taskmanager (76.5% contribution) → 72/100 🎯 High Confidence
   └─ Evidence: 23 .py files, Django ORM usage, REST APIs

⚠️ UNVERIFIED SKILLS (Resume Only)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Flask: 0/100 ✨ Not Detected
   Reason: No Flask imports or patterns found in analyzed repositories

💡 ADDITIONAL SKILLS (Code Only)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 JavaScript: 68/100 ⭐ Advanced
   Found in code but not mentioned in resume!
```
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
   -� How Code Analysis Works (Simple Explanation)

ChainCredit analyzes your code in 6 steps to verify your skills:

### Step 1: Git History Analysis
**What it checks:** Your actual code contributions in the repository.

**How it works:**
- Counts total commits in the repo
- Counts YOUR commits (by author name/email)
- Calculates contribution percentage: `(your_commits / total_commits) × 100`

**Example:**
```
Repository: ecommerce-app
Total commits: 150
Your commits: 120
Your contribution: 80%  ← You wrote most of the code!
```

---

### Step 2: Technology Detection
**What it checks:** Which programming languages and frameworks are used.

**How it works:**
- Scans file extensions (.py → Python, .jsx → React)
- Reads package files (package.json, requirements.txt)
- Searches for imports in code (import React, from django)

**Example:**
```
Files found:
├─ 15 .jsx files → React detected ✅
├─ 23 .py files → Python detected ✅
└─ 8 .css files → CSS detected ✅

Dependencies found:
├─ package.json: "react": "18.2.0" → React confirmed ✅
└─ requirements.txt: Django==4.2.0 → Django confirmed ✅
```

---

### Step 3: Skill Heuristic Scoring
**What it checks:** How well you actually use each technology (5 criteria, 20 points each).

**How it works for React:**
1. **Presence** (20 pts): Is React in package.json?
2. **Usage** (20 pts): Uses React hooks (useState, useEffect)?
3. **Size** (20 pts): How many .jsx files? (1/5/10+ files)
4. **Maturity** (20 pts): How many commits? (5/12/25+ commits)
5. **Authorship** (20 pts): Your contribution % (10%/30%/50%+ ownership)

**Example for React:**
```
✅ Presence (20/20): React found in package.json
✅ Usage (18/20): 8 React hooks detected (useState, useEffect, useContext)
✅ Size (20/20): 15 .jsx files found (threshold: 10+)
✅ Maturity (16/20): 18 commits (threshold: 12-25)
✅ Authorship (20/20): 80% contribution (threshold: 50%+)

Base Score: 94/100
```

---

### Step 4: Code Quality Checks
**What it checks:** How clean and maintainable your code is.

**How it works:**
- **Commit messages**: Descriptive messages (>20 chars) vs "fix" or "update"
- **Code complexity**: Average function length (<40 lines = good)
- **Documentation**: Comments ratio, README presence

**Example:**
```
Good commits: 45/50 (90%) ✅ → Clear commit messages
Avg function length: 32 lines ✅ → Well-structured code
Comments ratio: 15% ✅ → Decent documentation
```

---

### Step 5: Evidence Collection
**What it checks:** Specific proof of skill usage.

**How it works:**
- Searches for patterns in your code
- Records specific files using the technology
- Captures relevant code snippets

**Example for Django:**
```
Evidence collected:
├─ Files: models.py, views.py, urls.py, admin.py
├─ Imports: from django.db import models
├─ Patterns: 
│   ├─ Class User(models.Model) → ORM usage ✅
│   ├─ @api_view(['GET']) → REST API ✅
│   └─ admin.site.register(User) → Admin panel ✅
```

---

### Step 6: Contribution-Based Capping
**What it checks:** Do you have enough code ownership to claim this skill?

**How it works:**
Your final score is capped based on contribution percentage:
- **< 5%**: Insufficient → 0 points (you barely contributed)
- **< 10%**: Low → Max 40 points (minor contributor)
- **< 30%**: Medium → Max 60 points (regular contributor)
- **≥ 70%**: High → Max 100 points (major contributor)

**Example 1 - High Contribution:**
```
Repository: ecommerce-app
Your contribution: 100% (you're the only author)
Base heuristic score: 94/100
Contribution cap: 100 (high confidence)
Final Score: 94/100 ✅ Full credit
```

**Example 2 - Low Contribution:**
```
Repository: open-source-project
Your contribution: 8% (you made 2 small PRs)
Base heuristic score: 88/100
Contribution cap: 40 (low confidence)
Final Score: 40/100 ⚠️ Capped due to low contribution
```

**Example 3 - Insufficient Contribution:**
```
Repository: team-project
Your contribution: 3% (you fixed one typo)
Base heuristic score: 75/100
Contribution cap: 0 (insufficient)
Final Score: 0/100 ❌ Not enough contribution to claim skill
```

---

## 🧮 Multi-Repository Aggregation

**What it does:** Combines scores from all your repositories for each skill.

**How it works:**
Weighted average based on contribution percentage:

```
Skill: React
├─ ecommerce-app: 94/100 (contribution: 100%)
├─ portfolio: 72/100 (contribution: 85%)
└─ blog: 45/100 (contribution: 45%)

Weighted calculation:
= (94×100 + 72×85 + 45×45) / (100 + 85 + 45)
= (9400 + 6120 + 2025) / 230
= 17545 / 230
= 76/100 ⭐ Advanced

Final: React → 76/100 (averaged across 3 repositories)
```

---

## 🎯 Summary Example: Complete Flow

**Your resume claims:** "Python, React, Django, Flask"

**Step 1-2:** System analyzes your 2 GitHub repositories
- **ecommerce-app** (100% your code): React + Django detected
- **blog** (45% your code): React + Python detected

**Step 3-5:** Heuristic scoring with evidence
- React: 94/100 (ecommerce) + 62/100 (blog)
- Django: 88/100 (ecommerce)
- Python: 55/100 (blog)
- Flask: 0/100 (not detected anywhere)

**Step 6:** Contribution capping applied
- React in ecommerce: 94 → 94 (100% contribution ✅)
- React in blog: 62 → 60 (45% contribution, capped at 60 ⚠️)
- Django in ecommerce: 88 → 88 (100% contribution ✅)
- Python in blog: 55 → 55 (45% contribution, under cap ✅)
- Flask: 0 → 0 (not detected ❌)

**Final Report:**
```
✅ VERIFIED SKILLS:
  ├─ React: 84/100 (averaged, weighted by contribution)
  ├─ Django: 88/100
  └─ Python: 55/100

❌ UNVERIFIED SKILLS:
  └─ Flask: 0/100 (not detected in any repository)
```

---

## 🤝 Contributing

Want to add more technologies? Update these files:
- [scoring/skill_scorer.py](scoring/skill_scorer.py) - Add heuristic scoring criteria
- [scoring/skill_detector.py](scoring/skill_detector.py) - Add detection patterns
- [code_analysis/language_detector.py](code_analysis/language_detector.py) - Add file extensions

## 📄 License

MIT License

---

**Built with Python 🐍 | Powered by Gemini AI,