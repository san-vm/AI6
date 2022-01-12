from tkinter import *
from threading import Thread
import pyautogui
import sysTrayApp
import os
from time import sleep

font = 'Helvetica'
emptyMsg = "   "

# States
isOn = False
isFullScreen = False
isMovable = False


def renderFull():
	curWidth = width // 2
	curHeight = height // 2 - 100
	message.place(x=curWidth, y=curHeight + 120, anchor="center")
	triangle.place(x=curWidth, y=curHeight + 158, anchor="center")


def renderSmall():
	message.place(x=225, y=120, anchor="center")
	triangle.place(x=225, y=158, anchor="center")


def fullScreen():
	global isFullScreen
	isFullScreen = not isFullScreen

	if isFullScreen:
		renderFull()
		root.overrideredirect(0)
		root.attributes('-fullscreen', True)
		root.overrideredirect(1)
		return

	renderSmall()
	root.overrideredirect(1)
	root.attributes('-fullscreen', False)


def moveWindow():
	global isMovable
	root.overrideredirect(isMovable)
	isMovable = not isMovable


def dispMsg(strMsg: str, captialize=False, delay=0):
	if not isOn:
		return

	if captialize:
		strMsg = strMsg.upper()

	def disp(strMsg, delay):
		sleep(delay)
		global msg
		words = strMsg.split()
		for word in words:
			if len(word) < 3:
				delay = 500
			elif len(word) > 6:
				delay = 750
			else:
				delay = len(word) * 170

			msg.set(f' {word} ')
			sleep(delay / 1000)
		else:
			sleep(0.7)
			msg.set(emptyMsg)

	Thread(target=disp, args=[strMsg, delay]).start()


def load():
	Thread(target=sysTrayApp.handleVoice).start()


def keyHandle(e):
	key = e.keysym.upper()
	if key == 'X':
		if __name__ == '__main__':
			isOn = False
			os._exit(1)
		root.destroy()
	if key == 'M':
		moveWindow()
	elif key == 'F':
		fullScreen()


# Key Events
root = Tk()
msg = StringVar()
msg.set(emptyMsg)

message = Label(root, textvariable=msg, font=(font, 18, 'underline', 'bold'),
				bg="black", fg="white")

triangle = Button(root, text="▲", command=load, bg="black",
				  fg="red", border=0, font=(font, 18), activebackground="black", activeforeground="orange")


renderSmall()
root.bind("<KeyPress>", keyHandle)

# WinSize Calculations
width, height = pyautogui.size()
winWidth = int(((width) * 0.82) - 450//2)
winHeight = int(((height) * 0.2) - 250//2)

# Window Config
root.title('ProModders - AI6')
root.iconbitmap('./zImg/promodders.ico')
root.geometry(f'450x250+{winWidth}+{winHeight}')

root.attributes('-alpha', 0.8)
root.configure(background='black')
root.resizable(False, False)
root.overrideredirect(1)


def run():
	global isOn
	isOn = True
	dispMsg("What are your commands ?", 1, 1.5)
	root.mainloop()
