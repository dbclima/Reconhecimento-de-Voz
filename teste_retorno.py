import pyaudio
import numpy as np
import struct

FORMATIN = pyaudio.paFloat32
FORMATOUT = FORMATIN
CHANNELS = 1
RATE = 44100
CHUNK = 1024


audio = pyaudio.PyAudio()

# start Recording
streamIn = audio.open(format=FORMATIN, channels=CHANNELS,
                      rate=RATE, input=True, input_device_index=0,
                      frames_per_buffer=CHUNK)
streamOut = audio.open(format=FORMATOUT, channels=CHANNELS,
                       rate=RATE, output=True, input_device_index=0,
                       frames_per_buffer=CHUNK)


while True:
    break

    in_data = streamIn.read(CHUNK)
    print(np.array(struct.unpack('<1024f', in_data)).shape)
    streamOut.write(in_data)

in_data = np.load(r'Teste\Baixo.npy').flatten()
print(in_data, in_data.shape)

for i in range(100):
    data = in_data[i*1024: (i+1)*1024]
    data = struct.pack('<1024f', *data)
    streamOut.write(data)
