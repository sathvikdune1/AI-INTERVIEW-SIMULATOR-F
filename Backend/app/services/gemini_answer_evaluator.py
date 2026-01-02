import json
import re
from google.generativeai import GenerativeModel

model = GenerativeModel("gemini-1.5-flash")

def evaluate_answer(question: str, answer: str, category: str) -> dict:
    prompt = f"""
You are a senior interviewer.

Evaluate STRICTLY based on question type.

RULES:
- technical → correctness + depth
- aptitude → logic + correctness
- self_intro → clarity + relevance
- DO NOT evaluate coding here

Return ONLY valid JSON.

FORMAT:
{{
  "score": number (0-100),
  "strengths": [string],
  "weaknesses": [string],
  "suggestions": [string]
}}

QUESTION:
{question}

ANSWER:
{answer}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        json_text = re.search(r"\{.*\}", text, re.S).group()
        return json.loads(json_text)

    except Exception:
        return {
            "score": 50,
            "strengths": ["Answer attempted"],
            "weaknesses": ["Evaluation parsing failed"],
            "suggestions": ["Improve clarity, correctness, and structure"]
        }
