from gtts import gTTS
import os

# Text to convert to speech
text = "Welcome to the AI Interview Simulator. Your interview will begin shortly."

# Create TTS object
tts = gTTS(text=text, lang="en")

# Save audio file
tts.save("ai_voice.mp3")

# Play audio (Windows)
os.system("start ai_voice.mp3")

print("Text-to-Speech working successfully")
