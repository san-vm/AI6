from pyautogui import hotkey, press, write, keyDown, keyUp, click
import pyautogui as pyauto
import os
import pyttsx3
import datetime
import getpass
import facerec
import subprocess
from AIUI import dispMsg

uname = getpass.getuser()

engine = pyttsx3.init()
engine.setProperty("volume", 1)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

holdingKeys = False


def say(text):
	global engine
	engine.say(text)
	engine.runAndWait()


def holdingFunction(temp):
	global holdingKeys
	holdingKeys = []
	for i in temp:
		if i == "control":
			i = "ctrl"
		elif i in ["alternate", "alternative"]:
			i = "alt"
		else:
			continue
		holdingKeys.append(i)

	for i in holdingKeys:
		keyDown(i)


def releaseKeys():
	global holdingKeys
	if holdingKeys:
		for i in holdingKeys:
			keyUp(i)
		holdingKeys = False


def handleCmd(Text: str):
	global holdingKeys
	# Custom Commands
	if Text in ["open explorer", "explorer"]:
		subprocess.Popen("explorer")
	elif Text in ["open notepad", "notepad"]:
		subprocess.Popen("notepad")
	elif Text in ["open music", "music", "open spotify", "spotify"]:
		subprocess.Popen("spotify.exe")
	elif Text in ["open chrome", "chrome"]:
		os.system(' '.join([r'"C:\Program Files\Google\Chrome\Application\chrome.exe"',
							"--incognito", "--start-maximized"]))
	elif Text in ["open task manager", "task manager"]:
		os.system('taskmgr')
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
			hotkey("win", "m")
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
	elif Text in ["mouse click", "click mouse", "press mouse button"]:
		click()
	elif Text in ["press start", "click start"]:
		press("win")
	elif Text in ["press escape", "click escape"]:
		press("esc")
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
	elif Text in ["release keys", "release the hold", "release hold"]:
		releaseKeys()
	elif not Text.find("hold keys") or not Text.find("hold the keys"):
		temp = Text.split()
		i = temp[1] == "the"
		holdingFunction(temp[1 + i:])
	elif not Text.find("hot key"):
		keys = Text.split()[1:]
		hotkey(*keys)

	elif not Text.find("click") or not Text.find("press"):
		key = Text.split()[1:]
		for i in key:
			press(i)
		releaseKeys()
	elif not Text.find("type"):
		write(Text[5:])
	elif not Text.find("select all"):
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
