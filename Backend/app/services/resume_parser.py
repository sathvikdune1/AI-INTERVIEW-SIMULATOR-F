"""
Resume Parser Service
---------------------
- Extracts text from resume PDF
- Detects technical skills
- Calculates resume score (0–100)
"""

import fitz  # PyMuPDF

# -----------------------------
# Skill database
# -----------------------------
SKILLS_DB = [
    "python", "java", "c", "c++",
    "machine learning", "deep learning",
    "data science", "artificial intelligence",
    "aws", "azure", "gcp",
    "docker", "kubernetes",
    "sql", "mongodb", "mysql",
    "flask", "django", "fastapi",
    "nlp", "opencv", "tensorflow", "pytorch"
]

# -----------------------------
# PDF Text Extraction
# -----------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()

# -----------------------------
# Skill Extraction
# -----------------------------
def extract_skills(resume_text: str) -> list:
    found_skills = set()
    for skill in SKILLS_DB:
        if skill in resume_text:
            found_skills.add(skill)
    return sorted(found_skills)

# -----------------------------
# Resume Scoring (RAW)
# -----------------------------
def calculate_resume_score(skills: list) -> int:
    """
    Raw score calculation
    Each skill = 5 points
    """
    return min(len(skills) * 5, 100)

# -----------------------------
# Resume Analysis Wrapper
# -----------------------------
def analyze_resume(pdf_path: str) -> dict:
    resume_text = extract_text_from_pdf(pdf_path)
    skills = extract_skills(resume_text)

    score = calculate_resume_score(skills)

    return {
        "skills": skills,
        "score": score   # FINAL resume score (0–100)
    }
