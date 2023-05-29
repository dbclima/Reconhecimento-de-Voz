import pyaudio
import wave
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print('Inicio Gravação')

frames = []
tempo = 3

for i in range(0, int(RATE/CHUNK * tempo)):
    data = stream.read(CHUNK)
    frames.append(data)

print('Fim Gravação')

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(f'output/{str(time.time())}' + '.wav', 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

