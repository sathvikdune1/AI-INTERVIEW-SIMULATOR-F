import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime


def generate_pdf_report(interview: dict, output_dir: str) -> str:
    """
    Generates a professional PDF interview report
    and returns the file path.
    """

    filename = f"Interview_Report_{interview['_id']}.pdf"
    file_path = os.path.join(output_dir, filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 50

    # ---------------- HEADER ----------------
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "AI Interview Evaluation Report")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Generated On: {datetime.now().strftime('%d %b %Y %H:%M')}")
    y -= 40

    # ---------------- CANDIDATE INFO ----------------
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Candidate Details")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Name: {interview.get('name')}")
    y -= 15
    c.drawString(50, y, f"Email: {interview.get('email')}")
    y -= 15
    c.drawString(50, y, f"Mobile: {interview.get('mobile')}")
    y -= 15
    c.drawString(50, y, f"Job Role: {interview.get('job_role')}")
    y -= 15
    c.drawString(50, y, f"Difficulty: {interview.get('difficulty')}")
    y -= 30

    # ---------------- SCORES ----------------
    scores = interview.get("scores", {})

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Score Breakdown")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Resume Score: {scores.get('resume', 0)}")
    y -= 15
    c.drawString(50, y, f"Self Introduction: {scores.get('self_intro', 0)}")
    y -= 15
    c.drawString(50, y, f"Technical Score: {scores.get('technical', 0)}")
    y -= 15
    c.drawString(50, y, f"Aptitude Score: {scores.get('aptitude', 0)}")
    y -= 15
    c.drawString(50, y, f"Coding Score: {scores.get('coding', 0)}")
    y -= 15
    c.drawString(50, y, f"Proctoring Trust Score: {scores.get('proctoring', 100)}")
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"FINAL SCORE: {scores.get('final', 0)}")
    y -= 25

    # ---------------- DECISION ----------------
    decision = interview.get("decision", "N/A")

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, f"Final Decision: {decision}")
    y -= 40

    # ---------------- PROCTORING SUMMARY ----------------
    proctoring = interview.get("proctoring", {})
    violations = proctoring.get("total_violations", 0)

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Proctoring Summary")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Total Violations: {violations}")
    y -= 15
    c.drawString(50, y, f"Final Trust Score: {proctoring.get('final_trust_score', 100)}")

    # ---------------- FOOTER ----------------
    c.showPage()
    c.save()

    return file_path
