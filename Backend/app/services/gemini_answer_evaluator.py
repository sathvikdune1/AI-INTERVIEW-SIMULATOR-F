import json
import re
from google.generativeai import GenerativeModel

model = GenerativeModel("gemini-1.5-flash")


def evaluate_answer(question: str, answer: str, category: str) -> dict:

    prompt = f"""
You are a STRICT senior technical interviewer.

Evaluate the candidate answer carefully.

SCORING RUBRIC:

SELF INTRO
- communication clarity (30)
- relevance to role (30)
- structure and confidence (40)

TECHNICAL
- correctness (50)
- depth of explanation (30)
- technical terminology (20)

APTITUDE
- logical reasoning (40)
- correctness of solution (40)
- explanation clarity (20)

IMPORTANT RULES
- Score between 0 and 100
- Be strict like a real interviewer
- Short answers must receive low score
- Incorrect answers must receive low score
- Good structured answers receive high score

Return ONLY valid JSON.

FORMAT:
{{
"score": number,
"strengths": ["point1","point2"],
"weaknesses": ["point1","point2"],
"suggestions": ["point1","point2"]
}}

QUESTION:
{question}

CATEGORY:
{category}

CANDIDATE ANSWER:
{answer}
"""

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        match = re.search(r"\{.*\}", text, re.S)

        if not match:
            raise ValueError("Invalid JSON")

        result = json.loads(match.group())

        score = max(0, min(100, int(result.get("score", 50))))

        return {
            "score": score,
            "strengths": result.get("strengths", []),
            "weaknesses": result.get("weaknesses", []),
            "suggestions": result.get("suggestions", [])
        }

    except Exception as e:

        return {
            "score": 40,
            "strengths": ["Answer attempted"],
            "weaknesses": ["AI evaluation failed"],
            "suggestions": ["Provide clearer and more detailed answer"]
        }