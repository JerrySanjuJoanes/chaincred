# ChainCredit Quick Start Guide

## 🚀 Setup (5 minutes)

### 1. Install Dependencies
```bash
cd ChainCredit
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install GitPython pydriller numpy tqdm PyPDF2 python-docx google-genai
```

### 2. Get Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key

### 3. Configure API Key
```bash
# Copy the example file
cp .env.example .env

# Edit .env and replace 'your-api-key-here' with your actual key
nano .env  # or use any text editor
```

Your `.env` file should look like:
```
GEMINI_API_KEY=AIzaSyC_your_actual_key_here
```

## 📄 Prepare Your Resume

### Required Elements
Your resume **must include**:
- ✅ Full name
- ✅ GitHub repository URLs (full https://github.com/... links)
- ✅ List of technical skills

### Optional Elements
- Email address
- GitHub username
- Work experience
- Education

### Supported Formats
- PDF (`.pdf`)
- Microsoft Word (`.docx`)

### Example Resume Structure
```
JOHN DOE
john@example.com
GitHub: github.com/johndoe

SKILLS
Python, JavaScript, React, Django, Node.js

PROJECTS
- E-commerce App: https://github.com/johndoe/ecommerce
- Task Manager: https://github.com/johndoe/task-manager
```

## ▶️ Run Analysis

```bash
python main.py your_resume.pdf
```

## 📊 Understanding Results

### Stage 1: Resume Analysis
- Extracts your info using AI
- Finds GitHub repos automatically
- Shows detected skills

### Stage 2: Repository Analysis
For each repo found:
- Clones and analyzes your commits
- Calculates contribution percentage
- Scores your skills (0-100)
- Evaluates technology proficiency

### Stage 3: Skill Assessment Report
- **Overall stats**: Total commits, lines, files
- **Technology scores**: Averaged across all repos
- **Skill verification**: Compares resume vs actual code
  - ✅ Verified: Found in your code
  - ⚠️ Not Verified: Not found in analyzed repos
  - 💡 Additional: Found but not on resume

## 🎯 Skill Level Interpretation

| Score | Level | Meaning |
|-------|-------|---------|
| 80-100 | 🌟 Expert | Deep expertise, production-ready |
| 60-79 | ⭐ Advanced | Strong skills, independent work |
| 40-59 | 💫 Intermediate | Solid foundation, needs guidance |
| 0-39 | ✨ Beginner | Learning, requires supervision |

## ⚠️ Troubleshooting

### "GEMINI_API_KEY not found"
```bash
# Make sure you exported it:
echo $GEMINI_API_KEY  # Should show your key

# If empty, export again:
export GEMINI_API_KEY='your-key'
```

### "No GitHub repositories found"
- Check your resume includes **full URLs**
- Example: `https://github.com/username/repo` ✅
- Not: `github.com/username/repo` ⚠️

### "No contributions found"
Possible causes:
1. Your name in resume doesn't match Git commit name
2. You're not a contributor to those repos
3. Git username is different

**Solution**: Make sure Git commits use the same name as your resume

### "Repository not found"
- Check the repo URL is correct
- Make sure the repo is public (private repos require authentication)
- Remove any trailing characters (~, /, etc)

## 💡 Tips for Better Results

### 1. Use Your Real Repos
- Include repos where you have significant commits
- Quality > Quantity (3-5 substantial projects better than 20 forks)

### 2. Match Names
- Use the same name in resume and Git commits
- Or include GitHub username in resume

### 3. List Relevant Skills
- Focus on technologies actually used in your repos
- Be specific: "React" not just "Frontend"

### 4. Keep Resume Updated
- Add new projects as you build them
- Update skills list when you learn new tech

## 📞 Need Help?

Common issues:
1. **API errors**: Check API key is valid and has quota
2. **Parsing errors**: Ensure resume has clear sections
3. **Git errors**: Verify repo URLs are accessible

For complex issues, check:
- [AUDIT_REPORT.md](AUDIT_REPORT.md) - Technical details
- [README.md](README.md) - Full documentation
