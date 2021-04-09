# -- coding: utf-8 -- 
import io
import wave
import threading
import pyaudio
import numpy as np
from playsound import playsound
from threading import Thread
import glob
import asyncio

import virtual_assistant.cybervox as cybervox
import virtual_assistant.text_compare as text_compare
import virtual_assistant.key_actions as key_actions
from virtual_assistant.utils import log
from virtual_assistant.utils import config
from virtual_assistant.utils.download_media import download_media
import json

import pvporcupine
print(pvporcupine.KEYWORDS)
import struct
import time

logger = log.logger

handle = pvporcupine.create(keyword_paths=["hey_cyber_linux_2021-05-09-utc_v1_9_0.ppn"])
learing = {}
with open("learning/dictionary.json") as file:
    learing = json.load(file)
print(learing)
"""
    Configs
"""
RATE = handle.sample_rate # RATE / number of updates per second
CHUNK = handle.frame_length #int(RATE/20)
FORMAT = pyaudio.paInt16
CHANNELS = 1
frame_avg_filter_size = config.frame_avg_filter_size # The array bytes len average with audio to send

def _none():
    return

def play_confirmation():
    playsound("yea.wav")

def play_tsc():
    playsound("tsc.wav")
def find_action(text):
    if text in learing:
        print("TEXTO ENCONTRADO NO LEARNING FAZENDO DEPARA")
        text = learing[text]
        print("texto do comando : ", text)
    else:
        with open("commands.txt", 'a') as f:
            f.write(text)
            f.write("\n")
    all_actions = key_actions.get()
    logger.info('Finding action acording vox_text')
    best_text_compare = [.0, None]
    for action in all_actions:
        ratio_compare = text_compare.compare(text, action['name'])
        if ratio_compare >= 0.70:
            if best_text_compare[0] < ratio_compare:
                best_text_compare[0] = ratio_compare
                best_text_compare[1] = action
    return best_text_compare[1]
"""
    Frames are a array of bytes.
"""
def frames_to_binary_audio_input(frames, paudio):
    temp_file = io.BytesIO()

    with wave.open(temp_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(paudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    temp_file.seek(0)

    binary_audio = temp_file.read()
    return binary_audio

def play_audio(wav_binary):
    # file = '_.wav'
    # with open(file, 'wb') as f:
    #     f.write(wav_binary)
    # wave_obj = sa.WaveObject.from_wave_file('1.wav')
    playsound(wav_binary)
    # play_obj = wave_obj.play()
    # play_obj.wait_done()

async def listening(stream, paudio, vox_conn):
    logger.info('Speak "Jarvis" with strong Texas accent!!!')
    frames = []
    timer_start = None
    could_record = False
    started_timer = False
    could_send = False
    loop = asyncio.get_running_loop()
    while True:
        data = await loop.run_in_executor(None,stream.read,CHUNK)
        pcm = struct.unpack_from("h" * handle.frame_length, data)
        data_np = np.frombuffer(data, dtype=np.int16)
        peak = np.average(np.abs(data_np)) * 2
        filter = int(50 * peak/(2**16))

        """
            If frames size between FRAM_AVG_FILTER_SIZE send to cybervox
        """
        if (len(frames) > frame_avg_filter_size[0] and len(frames) < frame_avg_filter_size[1]):
            if could_send:
                logger.info('Aggregating wave bytes and send.')
                bytes_frames = frames_to_binary_audio_input(frames, paudio)
                logger.info('Upload to cybervox.')
                upload_payload = await cybervox.upload(vox_conn, bytes_frames)
                logger.info('Get uload_id.')
                vox_response = await cybervox.stt(vox_conn, upload_payload['upload_id'])
                logger.info('Cybervox response.')
                """
                    Finding action comparing action_name with vox_text
                """
                if vox_response['success']:
                    # First speak then send action.
                    action = find_action(vox_response['text'])
                    if action != None:
                        logger.info('Action', action)

                        if action['staticPayload']['response']:
                            text = action['staticPayload']['response']
                            logger.info('TTS: Speaking...')
                            """
                                TTS call
                            """
                            is_cache = glob.glob("cache/{}.wav".format(text))
                            if len(is_cache) > 0:
                                if text in glob.glob("cache/{}.wav".format(text))[0]:
                                    file = '{}/{}.wav'.format("cache", text)
                            else :
                                tts_response = await cybervox.tts(vox_conn, text)
                                wav_url = f"{config.cybervox_url}{tts_response['payload']['audio_url']}"
                                wav_binary = download_media(wav_url)
                                file = '{}/{}.wav'.format("cache",text)
                                with open(file, 'wb') as f:
                                    f.write(wav_binary)
                            play_audio(file)
                            key_actions.send(action)
                    else:
                        T = Thread(target=play_tsc)  # create thread
                        T.start()
                logger.info('Speak "Jarvis" with strong Texas accent!!!')
                """
                    Restart all variables if some sound was found.
                """
                frames = []
                timer_start = None
                could_record = False
                started_timer = False
                could_send = False

        """
            Filter "voice"
        """
        wake_up_word = handle.process(pcm)
        if wake_up_word >= 0:
            print("WAKE :" ,wake_up_word)
            T = Thread(target=play_confirmation)  # create thread
            T.start()
        if (wake_up_word >= 0 or could_record):
            if not started_timer:
                # playsound("yea.wav")
                logger.info('Speech command! Start timer and recording...')
                frames = []
                started_timer = True
                could_record = True
                timer_start = threading.Timer(2.7, _none)
                timer_start.setName('timer_start')
                timer_start.start()
                frames.append(data)

            if could_record:
                frames.append(data)


        if timer_start is not None:
            if not timer_start.is_alive():
                logger.info('If timer is disable, restart all variables')
                timer_start.cancel()
                timer_start = None
                could_record = False
                started_timer = False
                could_send = True

"""
    Starting microphone and listening audio
"""
def StreamPyAudio():
    paudio = pyaudio.PyAudio()
    info = paudio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (paudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", paudio.get_device_info_by_host_api_device_index(0, i).get('name'))
    stream = paudio.open(format=FORMAT,
                         channels=CHANNELS,
                         input_device_index=18,
                         rate=RATE,
                         input=True,
                         frames_per_buffer=CHUNK)
    return stream, paudio

async def main():
    logger.info('Starting...')
    """
        Start Pyaudio
    """
    stream, paudio = StreamPyAudio()
    """
        Start Cybervox
    """
    voxconn = await cybervox.conn()
    async with voxconn as websockets:
        voxstatus = await cybervox.ping(websockets)
        if voxstatus['success']:
            await listening(stream, paudio, websockets)
        stream.stop_stream()
        stream.close()
        paudio.terminate()

