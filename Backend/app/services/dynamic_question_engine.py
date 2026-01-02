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
Generate EXACTLY 10 interview questions in this strict order:
1 self-introduction
6 technical (NO math, NO puzzles)
1 aptitude (ONLY math/logical reasoning)
2 Python coding questions
Output ONLY a numbered list.
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
