import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SELF_INTRO_COUNT = 1
TECHNICAL_COUNT = 6
APTITUDE_COUNT = 1
CODING_COUNT = 2


def is_aptitude(q: str) -> bool:
    return bool(re.search(r"\b(cost|probability|ratio|number|how much|pattern)\b", q.lower()))


def is_coding(q: str) -> bool:
    return bool(re.search(r"\b(code|python|function|implement|write)\b", q.lower()))


def generate_interview_questions(resume_skills, job_role, difficulty):
    prompt = f"""
You are an expert technical interviewer.

Generate EXACTLY 10 HIGH-QUALITY interview questions for a {job_role} candidate.

STRICT RULES (DO NOT VIOLATE):

1. Question 1:
   - Self-introduction (professional, open-ended)

2. Questions 2–7 (6 questions):
   - Core TECHNICAL questions related to {job_role}
   - Cover concepts, real-world scenarios, and problem-solving
   - NO math puzzles
   - NO generic/basic questions

3. Question 8 (Aptitude – HARD level):
   - Must be logical reasoning OR quantitative aptitude
   - MUST be interview-level (like placements / competitive exams)
   - NOT simple arithmetic (avoid questions like 2+2, 2*4)
   - Should require thinking, not direct calculation

4. Questions 9–10 (2 Coding Questions):
   - Python coding problems ONLY
   - Must be real interview-level (medium to hard)
   - Include problem-solving, logic, or data structures
   - NO trivial problems (e.g., reverse string, add numbers)
   - Prefer array, string, hashmap, recursion, or algorithmic problems

OUTPUT FORMAT (STRICT):
- Only a numbered list (1 to 10)
- No explanations
- No headings
- No extra text

Ensure all questions are PROFESSIONAL, REALISTIC, and used in actual technical interviews.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=700
    )

    lines = [
        line.split(".", 1)[1].strip()
        for line in response.choices[0].message.content.split("\n")
        if line.strip() and line[0].isdigit()
    ]

    self_intro = [lines[0]]

    technical = []
    aptitude = []
    coding = []

    for q in lines[1:]:
        if is_coding(q):
            coding.append(q)
        elif is_aptitude(q):
            aptitude.append(q)
        else:
            technical.append(q)

    # 🔒 FORCE COUNTS
    return {
        "self_intro": self_intro[:1],
        "technical": technical[:6],
        "aptitude": aptitude[:1],
        "coding": coding[:2]
    }
