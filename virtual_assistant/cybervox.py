import time

import requests
import websockets

import virtual_assistant.cybervox_ping as cybervox_ping
import virtual_assistant.cybervox_stt as cybervox_stt
from virtual_assistant.utils import log
from virtual_assistant.utils import config

logger = log.logger

def getAccessToken(clientID, clientSecret):
    request = {
        'client_id':     clientID,
        'client_secret': clientSecret,
        'audience':      "https://api.cybervox.ai",
        'grant_type':    "client_credentials"
    }
    logger.debug("fetching access token...")
    response = requests.post("https://api.cybervox.ai/auth", json=request)
    if response.status_code != 200:
        return ""
    return response.json()['access_token']

async def ping(websocket):
    # --- PING ---
    ping_response = await cybervox_ping.ping(websocket)
    ping_payload = ping_response['payload']
    delta = time.time() - ping_payload['timestamp']
    logger.debug("   PING: Round-trip: %9.2f ms, Success: %s", delta * 1000.0, ping_payload['success'])
    return ping_payload

async def upload(websocket, name):
    # --- UPLOAD ---
    upload_response = await cybervox_stt.upload(websocket, name)
    upload_payload = upload_response['payload']
    delta = time.time() - upload_payload['timestamp']
    logger.debug(' UPLOAD: Round-trip: %9.2f ms, UploadID: %s',
                 delta * 1000.0,
                    upload_payload['upload_id'])
    return upload_payload

async def stt(websocket, uploadId):
    # --- STT ---
    stt_response = await cybervox_stt.stt(websocket, uploadId)
    stt_payload = stt_response['payload']
    delta = time.time() - stt_payload['timestamp']
    logger.debug('    STT: Round-trip: %9.2f ms, Success: %s, Reason: "%s", Text: "%s"',
                 delta * 1000.0,
                    stt_payload['success'],
                    stt_payload['reason'],
                    stt_payload['text'])
    return stt_payload


async def conn():
    client_id = config.client_id
    client_secret = config.client_secret
    if not client_id or not client_secret:
        logger.fatal('abort: check "CLIENT_ID" and "CLIENT_SECRET" env vars')
        return

    access_token = getAccessToken(client_id, client_secret)
    if not access_token:
        logger.fatal('abort: invalid access token')
        return

    return websockets.connect("wss://api.cybervox.ai/ws?access_token=" + access_token)
