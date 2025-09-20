import pvporcupine
import whisper
import os

porcupine = pvporcupine.create(
  access_key=os.getenv("PICO_VOICE"),
  keywords=['Hey Jarvis']
)

model = whisper.load_model("small")
result = model.transcribe("../samples/audio/Narakeet.mp3")
print(result["text"])

def get_next_audio_frame():
  pass

while True:
  audio_frame = get_next_audio_frame()
  keyword_index = porcupine.process(audio_frame)
  if keyword_index == 0:
      # detected `porcupine`
  elif keyword_index == 1:
      # detected `bumblebee`