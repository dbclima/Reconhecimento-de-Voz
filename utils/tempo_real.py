import pyaudio
import base64
import numpy as np
import matplotlib.pyplot as plt

# Quantas amostras por buffer
FRAMES_PER_BUFFER = 100
# Quantização
FORMAT = pyaudio.paInt16
# Audio modo
CHANNELS = 1
# Rate = amostragem
RATE = 1000
p = pyaudio.PyAudio()

plt.xlim((0, 1000))
plt.ylim((0, 1000))

stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

main_buffer = np.zeros((1000))
# print(main_buffer)

for i in range(1000):
    data = stream.read(FRAMES_PER_BUFFER)
    # print(data)
    audio = np.frombuffer(data, dtype=np.int16, count=FRAMES_PER_BUFFER)
    print(audio)
    main_buffer[:-1]
    main_buffer[i] = audio[0]
    # plt.scatter(i, audio[0], color='blue', s=1)

print(main_buffer)
stream.stop_stream()
stream.close()
