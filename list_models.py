from google import genai
from dotenv import load_dotenv
import os

load_dotenv()  # <-- THIS WAS MISSING

api_key = os.getenv("GEMINI_API_KEY")

print("API KEY FOUND:", bool(api_key))

client = genai.Client(api_key=api_key)

models = client.models.list()

for model in models:
    print(model.name)
