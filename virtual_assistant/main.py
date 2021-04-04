# -- coding: utf-8 -- 
import io
import wave
import threading
import pyaudio
import numpy as np
import simpleaudio as sa

import virtual_assistant.cybervox as cybervox
import virtual_assistant.text_compare as text_compare
import virtual_assistant.key_actions as key_actions
from virtual_assistant.utils import log
from virtual_assistant.utils import config
from virtual_assistant.utils.download_media import download_media

import pvporcupine
import struct

logger = log.logger

handle = pvporcupine.create(keywords=['jarvis'])

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

def find_action(text):
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
    file = '_.wav'
    with open(file, 'wb') as f:
        f.write(wav_binary)
    wave_obj = sa.WaveObject.from_wave_file(file)
    play_obj = wave_obj.play()
    play_obj.wait_done()

async def listening(stream, paudio, vox_conn):
    logger.info('Speak "Jarvis" with strong Texas accent!!!')
    frames = []
    timer_start = None
    could_record = False
    started_timer = False
    could_send = False

    while True:
        data = stream.read(CHUNK)
        
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
                            tts_response = await cybervox.tts(vox_conn, text)
                            wav_url = f"{config.cybervox_url}{tts_response['payload']['audio_url']}"
                            wav_binary = download_media(wav_url)
                            play_audio(wav_binary)
                            key_actions.send(action)
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
        if (wake_up_word >= 0 or could_record):
            if not started_timer:
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
    stream = paudio.open(format=FORMAT,
                         channels=CHANNELS,
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

