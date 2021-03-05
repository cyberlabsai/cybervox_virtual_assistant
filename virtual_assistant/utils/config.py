from environs import Env

env = Env()
env.read_env()
cybervox_url = env("CYBERVOX_URL", "")
client_id = env("CLIENT_ID", "")
client_secret = env("CLIENT_SECRET", "")
key_token = env("KEY_TOKEN", "")
key_portal = env("KEY_PORTAL", "")
assistant_name = env("ASSISTANT_NAME", "")
frame_avg_filter_size = [int(i) for i in env("FRAME_AVG_FILTER_SIZE", "").split(',')]
frame_avg_filter = [int(i) for i in env("FRAME_AVG_FILTER", "").split(',')]
