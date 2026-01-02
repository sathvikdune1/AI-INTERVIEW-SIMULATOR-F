from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import tempfile
import os

router = APIRouter()

class CodeRequest(BaseModel):
    language: str
    code: str

@router.post("/run")
def run_code(req: CodeRequest):
    try:
        with tempfile.TemporaryDirectory() as tmp:
            if req.language == "python":
                file = os.path.join(tmp, "main.py")
                open(file, "w").write(req.code)
                result = subprocess.run(
                    ["python", file],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

            elif req.language == "c":
                src = os.path.join(tmp, "main.c")
                exe = os.path.join(tmp, "a.out")
                open(src, "w").write(req.code)
                subprocess.run(["gcc", src, "-o", exe])
                result = subprocess.run([exe], capture_output=True, text=True)

            elif req.language == "cpp":
                src = os.path.join(tmp, "main.cpp")
                exe = os.path.join(tmp, "a.out")
                open(src, "w").write(req.code)
                subprocess.run(["g++", src, "-o", exe])
                result = subprocess.run([exe], capture_output=True, text=True)

            elif req.language == "java":
                src = os.path.join(tmp, "Main.java")
                open(src, "w").write(req.code)
                subprocess.run(["javac", src])
                result = subprocess.run(
                    ["java", "-cp", tmp, "Main"],
                    capture_output=True,
                    text=True
                )

            else:
                return {"output": "Unsupported language"}

            return {
                "output": result.stdout + result.stderr
            }

    except Exception as e:
        return {"output": str(e)}
