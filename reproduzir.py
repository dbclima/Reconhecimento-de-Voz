import tkinter.filedialog as fd
import pyaudio
import wave
from pathlib import Path

file = fd.askopenfilename(initialdir=Path('.'))
wf = wave.open(file, 'rb')

audio = pyaudio.PyAudio()

stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

CHUNK = 1024
data = wf.readframes(CHUNK)

while data:
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()
audio.terminate()
