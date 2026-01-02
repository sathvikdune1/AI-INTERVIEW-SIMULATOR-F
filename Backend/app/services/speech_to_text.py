import whisper
model = whisper.load_model("base")

def transcribe(audio_path):
    return model.transcribe(audio_path)["text"]
