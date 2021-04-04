from environs import Env

env = Env()
env.read_env()

client_id = env("CLIENT_ID", "")
client_secret = env("CLIENT_SECRET", "")
frame_avg_filter_size = [int(i) for i in env("FRAME_AVG_FILTER_SIZE", "").split(',')]