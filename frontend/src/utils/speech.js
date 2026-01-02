// frontend/src/utils/speech.js

export function speak(text) {
  if (!("speechSynthesis" in window)) {
    console.warn("Text-to-Speech not supported");
    return;
  }

  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 0.95;
  utterance.pitch = 1;
  utterance.volume = 1;

  const voices = window.speechSynthesis.getVoices();
  const preferred = voices.find(v =>
    v.name.toLowerCase().includes("english")
  );
  if (preferred) utterance.voice = preferred;

  window.speechSynthesis.speak(utterance);
}
