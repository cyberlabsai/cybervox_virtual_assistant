import pyaudio

p = pyaudio.PyAudio()
devices = []
for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    print("INPUT_DEVICE_INDEX: %s, DEVICE_NAME: %s" % (device['index'], device['name']))