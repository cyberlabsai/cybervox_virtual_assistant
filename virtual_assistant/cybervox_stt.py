import time 
import json

async def upload(ws, frames_bytes):
    """Send an upload request followed by a bytes stream on an established websocket connection.
    :param ws: an established websocket connection
    :param filename: the file name to be uploaded
    :return: the Upload response.
       >>> resp['payload']['upload_id']  # contains the upload identifier.
    """
    upload_request = {
        'emit':    "upload",
        'payload': {
            'max_uploads': 1,
            'timestamp':   int(time.time())
        }
    }
    await ws.send(json.dumps(upload_request))
    await ws.send(frames_bytes)
    return json.loads(await ws.recv())

async def stt(ws, upload_id):
    """Send a speech-to-text request on an established websocket connection.
    :param ws: an established websocket connection
    :param upload_id: the upload identifier returned by upload().
    :return: the STT response.
       >>> if resp['payload']['success'] is True then resp['payload']['text']  # contains the transcribed audio.
       >>> if resp['payload']['success'] is False then resp['payload']['reason']  # contains the failure reason.
    """
    stt_request = {
        'emit':    "stt",
        'payload': {
            'upload_id': upload_id,
            'timestamp': int(time.time())
        }
    }
    await ws.send(json.dumps(stt_request))
    return json.loads(await ws.recv())