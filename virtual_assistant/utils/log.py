import logging

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s'))

logger = logging.getLogger('main')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
