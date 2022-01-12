from time import sleep
from playsound import playsound
import json
from threading import Thread
import argparse
import queue
import sounddevice as sd
import vosk
import os
import sys
from zCmd import handleCmd

# Handle SR
isSRActive = False
selfMute = False
q = queue.Queue()


def int_or_str(text):
	"""Helper function for argument parsing."""
	try:
		return int(text)
	except ValueError:
		return text


def callback(indata, frames, time, status):
	"""This is called (from a separate thread) for each audio block."""
	if status:
		print(status, file=sys.stderr)
	q.put(bytes(indata))


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-l', '--list-devices', action='store_true',
					help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
	print(sd.query_devices())
	parser.exit(0)
parser = argparse.ArgumentParser(
	description=__doc__,
	formatter_class=argparse.RawDescriptionHelpFormatter,
	parents=[parser])
parser.add_argument(
	'-f', '--filename', type=str, metavar='FILENAME',
	help='audio file to store recording to')
parser.add_argument(
	'-m', '--model', type=str, metavar='MODEL_PATH',
	help='Path to the model')
parser.add_argument(
	'-d', '--device', type=int_or_str,
	help='input device (numeric ID or substring)')
parser.add_argument(
	'-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

if args.model is None:
	args.model = "model"
if not os.path.exists(args.model):
	print("Find 'model' in the current folder.")
	parser.exit(0)
if args.samplerate is None:
	device_info = sd.query_devices(args.device, 'input')
	# soundfile expects an int, sounddevice provides a float:
	args.samplerate = int(device_info['default_samplerate'])
model = vosk.Model(args.model)


def stopSR():
	global isSRActive
	isSRActive = False
	playsound('./zImg/beep.wav')


def selfMuteCall():
	global selfMute
	selfMute = False
	sleep(2)
	selfMute = True


rec = vosk.KaldiRecognizer(model, args.samplerate)


def speechRecognition():
	global selfMute, q, isSRActive, rec
	isSRActive = True
	selfMute = False
	Thread(target=selfMuteCall).start()

	try:
		with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device, dtype='int16',
							   channels=1, callback=callback):

			while isSRActive:
				data = q.get()
				q = queue.Queue()
				if rec.AcceptWaveform(data):
					curCmd = json.loads(rec.Result())
					if (not curCmd["text"]) and selfMute:
						stopSR()
						return

					isSRActive = False
					return handleCmd(curCmd["text"])
			else:
				q = queue.Queue()

	except Exception as e:
		parser.exit(type(e).__name__ + ':::: ' + str(e))
