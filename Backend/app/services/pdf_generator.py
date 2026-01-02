"""
PDF Interview Report Generator
------------------------------
Generates a professional PDF report for each interview
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def generate_interview_pdf(interview_data: dict, output_dir="reports"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{interview_data['candidate_name'].replace(' ', '_')}_Interview_Report.pdf"
    filepath = os.path.join(output_dir, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    y = height - 50

    def draw_line(text):
        nonlocal y
        c.drawString(40, y, text)
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 50

    # ---------- TITLE ----------
    c.setFont("Helvetica-Bold", 18)
    draw_line("AI Interview Evaluation Report")
    y -= 10

    c.setFont("Helvetica", 11)
    draw_line(f"Candidate Name: {interview_data['candidate_name']}")
    draw_line(f"Role: {interview_data['role']}")
    draw_line(f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    y -= 10

    # ---------- QUESTION & ANSWER ----------
    c.setFont("Helvetica-Bold", 12)
    draw_line("Interview Question:")
    c.setFont("Helvetica", 11)
    draw_line(interview_data["question"])
    y -= 8

    c.setFont("Helvetica-Bold", 12)
    draw_line("Candidate Answer:")
    c.setFont("Helvetica", 11)
    draw_line(interview_data["answer"])
    y -= 10

    # ---------- SCORES ----------
    c.setFont("Helvetica-Bold", 12)
    draw_line("Scores:")
    c.setFont("Helvetica", 11)

    scores = interview_data["scores"]
    draw_line(f"Resume Score       : {scores['resume']}")
    draw_line(f"NLP Score          : {scores['nlp']}")
    draw_line(f"Coding Score       : {scores['coding']}")
    draw_line(f"Emotion Score      : {scores['emotion']}")
    draw_line(f"Communication Score: {scores['communication']}")
    draw_line(f"Final Score        : {scores['final']}")

    y -= 8
    c.setFont("Helvetica-Bold", 12)
    draw_line(f"Final Decision: {interview_data['decision']}")

    y -= 10

    # ---------- FEEDBACK ----------
    c.setFont("Helvetica-Bold", 12)
    draw_line("AI Feedback:")
    c.setFont("Helvetica", 11)

    for line in interview_data["feedback"].split("\n"):
        draw_line(line)

    c.save()
    return filepath
