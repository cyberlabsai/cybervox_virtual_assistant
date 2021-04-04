import asyncio
import pyaudio
import uvloop
import numpy as np

import config

"""
    Configs
"""
RATE = 44100
CHUNK = int(RATE/20) # RATE / number of updates per second
FORMAT = pyaudio.paInt16
CHANNELS = 1
frame_avg_filter = config.frame_avg_filter # The array bytes average with audio to filter
frame_avg_filter_size = config.frame_avg_filter_size # The array bytes len average with audio to send

"""
    calibrate_filter
"""

def f():
    return

async def listening(stream, paudio):
    while True:
        data = stream.read(CHUNK)
        dataNp = np.fromstring(data, dtype=np.int16)
        peak = np.average(np.abs(dataNp)) * 2
        filter = int(50 * peak/(2**16))
        """
            Draw sound waves
        """
        bars = "=" * filter
        print("%s - %s" % (filter, bars))
"""
    Starting microphone and listening audio
"""
def StreamPyAudio():
    paudio = pyaudio.PyAudio()
    stream = paudio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    return stream, paudio

async def main():
    """
        Start Pyaudio
    """
    stream, paudio = StreamPyAudio()
    await listening(stream, paudio)
    stream.stop_stream()
    stream.close()
    paudio.terminate()

if __name__=="__main__":
    uvloop.install()
    asyncio.run(main())