import requests

JUDGE0_URL = "https://ce.judge0.com/submissions/?wait=true"

# Sample code submitted by candidate
source_code = """
print("Hello from AI Interview Simulator")
"""

payload = {
    "language_id": 71,  # Python
    "source_code": source_code
}

response = requests.post(JUDGE0_URL, json=payload)

result = response.json()

print("Status:", result["status"]["description"])
print("Output:", result["stdout"])
