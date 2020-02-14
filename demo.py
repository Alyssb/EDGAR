import sys
sys.path.append('./CSC450/')
from audioMetrics import get_Metrics
from spectrogram import get_spectrogram

sys.path.append('./recording_audio/')
from record_audio import record_audio

input_name = record_audio()
print("Audio file: " + input_name + " created")
get_Metrics(input_name ,0, 512, 128, "delta")
get_spectrogram(input_name, 0)