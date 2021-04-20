from environs import Env

env = Env()
env.read_env()
cybervox_url = env("CYBERVOX_URL", "")
client_id = env("CLIENT_ID", "")
client_secret = env("CLIENT_SECRET", "")
key_token = env("KEY_TOKEN", "")
key_portal = env("KEY_PORTAL", "")
input_device_index = env("INPUT_DEVICE_INDEX", "")
frame_avg_filter_size = [int(i) for i in env("FRAME_AVG_FILTER_SIZE", "").split(',')]
wake_up_word = int(env("WAKE_UP_WORD", 0))