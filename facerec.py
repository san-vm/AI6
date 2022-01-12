import cv2 as cv
import cvzone as cvz

cascadeFace = cv.CascadeClassifier(
	cv.data.haarcascades + "haarcascade_frontalface_alt.xml")
cascadeEyes = cv.CascadeClassifier(
	cv.data.haarcascades + "haarcascade_eye.xml")
cascadeUB = cv.CascadeClassifier(
	cv.data.haarcascades + "haarcascade_upperbody.xml")

adminOverlay = cv.imread("./zImg/admin.png", cv.IMREAD_UNCHANGED)
famOverlay = cv.imread("./zImg/fam.png", cv.IMREAD_UNCHANGED)
threatOverlay = cv.imread("./zImg/threat.png", cv.IMREAD_UNCHANGED)
unknownOverlay = cv.imread("./zImg/nonThreat.png", cv.IMREAD_UNCHANGED)


def face():
	isUnknown = True
	isAdmin = isFam = isThreat = False
	showFace = True
	showUB = showEye = False
	cap = cv.VideoCapture(0, cv.CAP_DSHOW)
	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))

	size = (frame_width, frame_height)
	vid = cv.VideoWriter('filename.avi', cv.VideoWriter_fourcc(*'MJPG'), 24, size)

	while True:
		_, img = cap.read()
		if not _:
			break
		gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

		if showFace:
			faces = cascadeFace.detectMultiScale(gray, 1.1, 4)
			for x, y, w, h in faces:
				# cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 200), 4)

				try:
					if isThreat:
						temp = cv.resize(threatOverlay, (w+70, h+70))
						img = cvz.overlayPNG(img, temp, [x-35, y-10])
					elif isAdmin:
						temp = cv.resize(adminOverlay, (w+70, h+70))
						img = cvz.overlayPNG(img, temp, [x-35, y-35])
					elif isFam:
						temp = cv.resize(famOverlay, (w+70, h+70))
						img = cvz.overlayPNG(img, temp, [x-35, y-35])
					elif isUnknown:
						temp = cv.resize(unknownOverlay, (w+70, h+70))
						img = cvz.overlayPNG(img, temp, [x-35, y-35])
				except:
					pass

				if showEye:
					roi_eye = gray[y:y+h, x:x+w]
					roi_color = img[y:y+h, x:x+w]
					eyes = cascadeEyes.detectMultiScale(roi_eye)
					for x, y, w, h in eyes:
						cv.rectangle(roi_color, (x, y),
									 (x + w, y + h), (150, 255, 0), 2)


		if showUB:
			UB = cascadeUB.detectMultiScale(gray)
			for x, y, w, h in UB:
				cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 8)

		if len(faces):
			vid.write(img)
		cv.imshow('AI6', img)

		key = cv.waitKey(1)
		if key != -1:
			key = key & 0xff
			if key in (27, ord('q'), ord('Q')):
				break
			elif key in (ord('e'), ord('E')):
				showEye = not showEye
			elif key in (ord('f'), ord('F')):
				showFace = not showFace
			elif key in (ord('b'), ord('B')):
				showUB = not showUB
			elif key in (ord('t'), ord('T')):
				isThreat = not isThreat
				isAdmin = not isAdmin

	cap.release()
	vid.release()
	cv.destroyAllWindows()


if __name__ == '__main__':
	face()
