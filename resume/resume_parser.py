"""
Resume parsing using Gemini API to extract skills and GitHub repositories.
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import PyPDF2
import google.genai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def configure_gemini() -> genai.Client:
    """Create a Gemini client using API key from environment."""
    # Hardcoded fallback per user request; environment variable still preferred
    api_key = os.getenv('GEMINI_API_KEY') or "AIzaSyAB4wYkNbC6Mm45J-HOEpevI4YkfNhXXuA"
    return genai.Client(api_key=api_key)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF file.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text content
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")
    
    return text


def extract_hyperlinks_from_pdf(pdf_path: str) -> List[str]:
    """
    Extract hyperlinks (URLs) from PDF file using PyMuPDF.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        List of URLs found in PDF hyperlinks
    """
    urls = []
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        
        for page in doc:
            links = page.get_links()
            for link in links:
                if 'uri' in link:
                    url = link['uri']
                    # Only keep GitHub URLs
                    if 'github.com' in url.lower():
                        urls.append(url)
        
        doc.close()
    except ImportError:
        print("⚠️  PyMuPDF not installed. Run: pip install PyMuPDF")
    except Exception as e:
        print(f"⚠️  Could not extract hyperlinks: {e}")
    
    return urls


def extract_text_from_doc(doc_path: str) -> str:
    """
    Extract text from DOC/DOCX file.
    
    Args:
        doc_path: Path to DOC/DOCX file
        
    Returns:
        Extracted text content
    """
    try:
        import docx
        doc = docx.Document(doc_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except ImportError:
        raise ImportError("python-docx not installed. Install with: pip install python-docx")
    except Exception as e:
        raise ValueError(f"Error reading DOC: {e}")


def parse_resume_with_regex(resume_text: str) -> Dict:
    """
    Simple regex-based resume parser (fallback when Gemini unavailable).
    
    Args:
        resume_text: Raw text from resume
        
    Returns:
        Dictionary with name, email, skills, and github_repos
    """
    import json
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, resume_text)
    email = emails[0] if emails else ''
    
    # Extract GitHub repos
    github_repos = extract_github_urls(resume_text)
    
    # Extract GitHub username
    github_username = ''
    username_pattern = r'github\.com/([A-Za-z0-9\-]+)'
    usernames = re.findall(username_pattern, resume_text.lower())
    if usernames:
        github_username = usernames[0]
    
    # Extract name (first line usually, or first capitalized phrase)
    lines = [l.strip() for l in resume_text.split('\n') if l.strip()]
    candidate_name = lines[0] if lines else 'Unknown'
    
    # Extract skills (common keywords)
    common_skills = [
        'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'Rust',
        'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask', 'FastAPI',
        'Spring', 'TailwindCSS', 'Bootstrap', 'HTML', 'CSS', 'SQL', 'MongoDB', 
        'PostgreSQL', 'MySQL', 'Redis', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
        'Git', 'Linux', 'REST', 'GraphQL', 'API', 'Machine Learning', 'AI', 'Data Science'
    ]
    
    skills = []
    text_upper = resume_text.upper()
    for skill in common_skills:
        if skill.upper() in text_upper:
            skills.append(skill)
    
    return {
        'candidate_name': candidate_name,
        'email': email,
        'github_username': github_username,
        'skills': skills,
        'github_repos': github_repos
    }


def parse_resume_with_gemini(resume_text: str) -> Dict:
    """
    Parse resume using Gemini API to extract structured information.
    Falls back to regex parser if API fails.
    
    Args:
        resume_text: Raw text from resume
        
    Returns:
        Dictionary with name, email, skills, and github_repos
    """
    try:
        client = configure_gemini()
        
        # Use a supported public model name for google-genai
        model_name = 'gemini-2.0-flash-exp'
        
        prompt = f"""
You are a resume parser. Extract the following information from this resume and return ONLY valid JSON:

1. candidate_name: Full name of the candidate
2. email: Email address
3. github_username: GitHub username if mentioned (just the username, not full URL)
4. skills: List of technical skills (programming languages, frameworks, tools)
5. github_repos: List of GitHub repository URLs mentioned in the resume

Resume text:
{resume_text}

Return ONLY a JSON object in this exact format (no markdown, no code blocks):
{{
  "candidate_name": "Name Here",
  "email": "email@example.com",
  "github_username": "username",
  "skills": ["Python", "JavaScript", "React", "Django"],
  "github_repos": ["https://github.com/user/repo1", "https://github.com/user/repo2"]
}}

If any field is not found, use empty string for strings or empty array for lists.
If any field is not found, use empty string for strings or empty array for lists.
"""
        
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        # google-genai returns candidates list; pick first text
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        response_text = re.sub(r'^```json\s*', '', response_text)
        response_text = re.sub(r'^```\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
        
        # Parse JSON
        import json
        data = json.loads(response_text)
        
        # Validate and clean data
        result = {
            'candidate_name': data.get('candidate_name', 'Unknown'),
            'email': data.get('email', ''),
            'github_username': data.get('github_username', ''),
            'skills': data.get('skills', []),
            'github_repos': data.get('github_repos', [])
        }
        
        # If no repos found but github_username exists, try to find repos
        if not result['github_repos'] and result['github_username']:
            # Extract URLs from raw text as fallback
            urls = extract_github_urls(resume_text)
            result['github_repos'] = urls
        
        return result
        
    except Exception as e:
        print(f"\n⚠️  Gemini API unavailable ({str(e)[:100]}...)")
        print("📝 Falling back to regex-based parser...")
        return parse_resume_with_regex(resume_text)


def classify_github_url(url: str) -> Dict[str, str]:
    """
    Classify a GitHub URL as either a profile or repository.
    
    Args:
        url: GitHub URL to classify
        
    Returns:
        Dictionary with 'type' ('profile' or 'repository') and 'url'
    """
    # Clean URL
    url = url.rstrip('/').replace('.git', '')
    
    # Pattern for repository: https://github.com/username/repo
    repo_pattern = r'https?://github\.com/([A-Za-z0-9\-]+)/([A-Za-z0-9\-\._]+)$'
    # Pattern for profile: https://github.com/username
    profile_pattern = r'https?://github\.com/([A-Za-z0-9\-]+)$'
    
    if re.match(repo_pattern, url):
        return {'type': 'repository', 'url': url}
    elif re.match(profile_pattern, url):
        return {'type': 'profile', 'url': url}
    else:
        # Unknown format - might be a repo with subpaths
        parts = url.replace('https://github.com/', '').replace('http://github.com/', '').split('/')
        if len(parts) >= 2:
            return {'type': 'repository', 'url': url}
        else:
            return {'type': 'unknown', 'url': url}


def extract_github_urls(text: str) -> List[str]:
    """
    Extract GitHub repository URLs from text using regex.
    
    Args:
        text: Text to search
        
    Returns:
        List of GitHub repository URLs (excludes profile URLs)
    """
    pattern = r'https?://github\.com/[\w\-]+(?:/[\w\-\.]+)?'
    urls = re.findall(pattern, text)
    
    # Remove duplicates and clean
    urls = list(set(urls))
    # Remove trailing slashes and .git
    urls = [url.rstrip('/').replace('.git', '') for url in urls]
    
    # Filter only repository URLs
    repo_urls = []
    for url in urls:
        classification = classify_github_url(url)
        if classification['type'] == 'repository':
            repo_urls.append(url)
    
    return repo_urls


def parse_resume_file(file_path: str) -> Dict:
    """
    Parse resume file and extract structured information.
    
    Args:
        file_path: Path to resume file (PDF or DOC/DOCX)
        
    Returns:
        Dictionary with candidate info, skills, and repos
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Resume file not found: {file_path}")
    
    # Extract text based on file type
    ext = file_path.suffix.lower()
    
    if ext == '.pdf':
        text = extract_text_from_pdf(str(file_path))
        # Also extract hyperlinks from PDF
        hyperlink_urls = extract_hyperlinks_from_pdf(str(file_path))
    elif ext in ['.doc', '.docx']:
        text = extract_text_from_doc(str(file_path))
        hyperlink_urls = []
    else:
        raise ValueError(f"Unsupported file format: {ext}. Use PDF or DOC/DOCX")
    
    if not text.strip():
        raise ValueError("No text could be extracted from the resume")
    
    # Parse with Gemini
    print("📄 Parsing resume with Gemini API...")
    parsed_data = parse_resume_with_gemini(text)
    
    # Merge hyperlinks with extracted repos
    if hyperlink_urls:
        print(f"   📎 Found {len(hyperlink_urls)} hyperlink(s) in PDF")
        all_repos = set(parsed_data['github_repos'] + hyperlink_urls)
        parsed_data['github_repos'] = list(all_repos)
    
    print(f"\n✅ Resume Parsed Successfully!")
    print(f"   Candidate: {parsed_data['candidate_name']}")
    print(f"   Email: {parsed_data['email']}")
    print(f"   GitHub Username: {parsed_data['github_username']}")
    print(f"   Skills Found: {len(parsed_data['skills'])}")
    print(f"   GitHub Repos Found: {len(parsed_data['github_repos'])}")
    
    if parsed_data['skills']:
        print(f"   Skills: {', '.join(parsed_data['skills'][:5])}{'...' if len(parsed_data['skills']) > 5 else ''}")
    
    if not parsed_data['github_repos']:
        print("\n⚠️  Warning: No GitHub repositories found in resume")
        print("   Make sure your resume includes GitHub project URLs")
    
    return parsed_data
