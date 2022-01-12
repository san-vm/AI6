from pyautogui import hotkey, press, write
import pyautogui as pyauto
import os
import pyttsx3
import datetime
import getpass
import facerec
from AIUI import dispMsg

uname = getpass.getuser()

engine = pyttsx3.init()
engine.setProperty("volume", 1)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def say(text):
	global engine
	engine.say(text)
	engine.runAndWait()


def handleCmd(Text: str):
	# Custom Commands
	if Text == "open explorer":
		os.system("explorer")
	elif Text == "open chrome":
		os.system(' '.join([r'"C:\Program Files\Google\Chrome\Application\chrome.exe"',
						   "--incognito", "--start-maximized"]))
	elif Text == "open utilities":
		hotkey('alt', '0')
	elif Text in ["can you see me", "open camera"]:
		facerec.face()

	# Navigations
	elif Text in ["close window", "close this window", "closed window"]:
		hotkey("alt", "f4")
	elif "maximize" in Text:
		hotkey("win", "up")
	elif "minimize" in Text:
		if "this window" in Text:
			hotkey("win", "down")
			hotkey("win", "down")
		else:
			hotkey("win", "d")
	elif Text in ["switch window", "such window", "switch windows", "such windows"]:
		hotkey('alt', 'tab')
	elif Text in ["shut down", "power off", "power down"]:
		os.system("shutdown /p")
	elif Text in ["restart", "reboot"]:
		os.system("shutdown /r /t 0")
	elif Text in ["lock screen", "lock computer"]:
		os.system("Rundll32.exe user32.dll,LockWorkStation")
	elif Text in ["sleep", "turn off display", "screen off"]:
		press("sleep")

	# Keyboard
	elif Text in ["press start", "click start"]:
		press("win")
	elif Text in ["press next", "press next track", "click next"]:
		press("nexttrack")
	elif Text in ["press previous", "press previous track", "click previous"]:
		press("prevtrack")
	elif Text in ["play", "press play", "click play", "pause", "press pause", "click pause"]:
		press("playpause")
	elif Text in ["mute", "mute volume"]:
		press("volumemute")
	elif Text in ["increase volume", "volume", "volume up"]:
		press("volumeup")
	elif Text in ["decrease volume", "reduce volume"]:
		press("volumedown")
	elif Text in ["press options", "options"]:
		press("option")

	elif "click" in Text or "press" in Text:
		key = Text.split()[1].lower()
		press(key)
	elif "type" in Text:
		splits = Text.split()
		if splits[0].lower() == "type":
			write(Text[5:])
	elif "select all" in Text:
		hotkey('ctrl', 'a')
	elif Text in ["sure all windows", "show all windows", "so all windows"]:
		hotkey("win", "tab")

	# Systems
	elif Text in ["hello", "hi", "hey"]:
		dispMsg("what's up", 1)
		say("what's up")

	elif Text in ["snapshot", "screen shot"]:
		now = datetime.datetime.now()
		timestamp = str(int(datetime.datetime.timestamp(now)))
		path = os.path.join("C:\\", "Users", uname,
							"Desktop", timestamp + '.png')
		pyauto.screenshot(path)
		os.startfile(path)

	elif Text in ["what's that time", "what's the time", "what time"]:
		date_time = datetime.datetime.now()
		tempDate = date_time.strftime("%I:%M")
		dispMsg(tempDate)
		say(tempDate)

	elif Text in ["what's that date", "what's the date", "what date"]:
		date_time = datetime.datetime.now()
		tempTime = date_time.strftime("%e! %A")
		dispMsg(tempTime)
		say(tempTime)

	elif Text in ["exit speech recognition", "goodbye", "sleep", "bye", "see you"]:
		dispMsg('. ..')
		say("C you")
		return True

	# Custom shortcuts
	elif Text in ["change speaker", "change speakers", "change is speaker"]:
		hotkey("ctrl", "`")
	else:
		os.system('cls')
		print(Text)
		say(Text)


# def runOCR(tempPath):
# 	pytesseract.tesseract_cmd = basedir + r'\Tesseract-OCR\tesseract.exe'
# 	img = Image.open(tempPath)
# 	# Simple image to string
# 	thresh = 125
# 	def fn(x): return 255 if x > thresh else 0
# 	img = img.convert('L').point(fn, mode='1')
# 	strImg = pytesseract.image_to_string(img).split('\n')
# 	strImg = [x.strip() for x in strImg if x.strip()]
