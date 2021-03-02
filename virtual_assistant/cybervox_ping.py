import time
import json

async def ping(ws):
    """Send a ping request on an established websocket connection.
    :param ws: an established websocket connection
    :return: the ping response
    """
    ping_request = {
        'emit':    "ping",
        'payload': {
            'timestamp': int(time.time())
        }
    }
    await ws.send(json.dumps(ping_request))
    return json.loads(await ws.recv())
