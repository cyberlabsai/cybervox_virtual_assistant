import requests
from jinja2 import Template

from virtual_assistant.utils import log
from virtual_assistant.utils import config

logger = log.logger
def send(action):
    try:
        logger.info('Send action')
        headers = {'content-type': 'application/json'}
        response = requests.request(action['method'], action['url'], headers=headers)
        if response.status_code != '200':
            logger.warning("Status code %i" % response.status_code)
        print(response.body)
    except:
        logger.error("Ops! Error :/")
def get():
    logger.info('Requesting portals actions')
    with open('virtual_assistant/templates/portal.json.jinja') as f:
        payload = Template(f.read())
    body = payload.render(key_token=config.key_token, key_portal=config.key_portal)
    headers = {'content-type': 'application/json'}
    response = requests.request("POST", 'https://api.prd.keyapp.ai/key/v1', data=body, headers=headers)
    if response.status_code != 200:
        logger.warning('Error on getPortals request.')
        logger.warning("Status code %i" % response.status_code)
        logger.warning(response.json())
        return ''
    json = response.json()
    if json['data']['getPortals']['status']:
        logger.info('Portal found! Rerturning portal actions')
        return json['data']['getPortals']['portals'][0]['actions']
    return ''