import os
import sys
from PySide2 import QtWidgets, QtGui
from threading import Thread
import AI6
import onWake
import subprocess
import host


def handleVoice():
	if onWake.isSRActive:
		onWake.stopSR()
		return
	AI6.isVoiceActive = False
	AI6.loadVoice()
	AI6.isVoiceActive = True
	Thread(target=AI6.main).start()


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
	def __init__(self, icon, parent=None):
		QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
		self.setToolTip(f'ProModders - AIONE')
		menu = QtWidgets.QMenu(parent)

		open_app = menu.addAction("Notepad")
		open_app.triggered.connect(self.open_notepad)
		open_app.setIcon(QtGui.QIcon("./zImg/icon.png"))

		open_cal = menu.addAction("Open Calculator")
		open_cal.triggered.connect(self.open_calc)
		open_cal.setIcon(QtGui.QIcon("./zImg/icon.png"))

		exit_ = menu.addAction("Exit")
		exit_.triggered.connect(lambda: os._exit(1))
		exit_.setIcon(QtGui.QIcon("./zImg/icon.png"))

		menu.addSeparator()
		self.setContextMenu(menu)
		self.activated.connect(self.onTrayIconActivated)

	def onTrayIconActivated(self, reason):
		if reason == self.Trigger:
			Thread(target=handleVoice).start()

	def open_notepad(self):
		subprocess.Popen(['notepad'])

	def open_calc(self):
		subprocess.Popen(['calc'])


def mainApp():
	app = QtWidgets.QApplication(sys.argv)
	w = QtWidgets.QWidget()
	tray_icon = SystemTrayIcon(QtGui.QIcon("./zImg/icon.png"), w)
	tray_icon.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	Thread(target=mainApp).start()
	Thread(target=AI6.main).start()
	Thread(target=host.mainf).start()
	import AIUI
	AIUI.run()
