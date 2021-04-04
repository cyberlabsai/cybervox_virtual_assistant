import time
import json

async def tts(ws, text):
    """Send a text-to-speech request on an established websocket connection.
    :param ws: an established websocket connection
    :param text: the text to be converted to an WAVE file
    :return: the TTS response.
       >>> if resp['payload']['success'] is True then resp['payload']['audio_url']  # contains the converted audio URL.
       >>> if resp['payload']['success'] is False then resp['payload']['reason']  # contains the failure reason.
    """
    tts_request = {
        'emit':    "tts",
        'payload': {
            'text':      text,
            'timestamp': int(time.time())
        }
    }
    await ws.send(json.dumps(tts_request))
    return json.loads(await ws.recv())