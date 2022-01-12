import struct
import pyaudio
import pvporcupine
from playsound import playsound
import os

from onWake import speechRecognition as sr

# os.system("cls")
print("\t\tWelcome AI6\n\t\t ---------")

isVoiceActive = True

try:
	porcupine = pvporcupine.create(keywords=["alexa"])
	pa = pyaudio.PyAudio()
	audio_stream = pa.open(
		rate=porcupine.sample_rate,
		channels=1,
		format=pyaudio.paInt16,
		input=True,
		frames_per_buffer=porcupine.frame_length)

except Exception as e:
	print(e)


def loadVoice():
	playsound('./zImg/note.wav')
	if sr():
		os._exit(1)


def main():
	global isVoiceActive
	try:
		while isVoiceActive:
			pcm = audio_stream.read(porcupine.frame_length)
			pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
			keyword_index = porcupine.process(pcm)

			if keyword_index >= 0:
				loadVoice()

	except Exception as e:
		print(e)


if __name__ == '__main__':
	main()
