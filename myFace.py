import cv2 as cv
import cvzone as cvz
import face_recognition as fr
import datetime
import getpass
import os

# Constants
uname = getpass.getuser()
curDir = os.getcwd()
people = []

if not os.path.exists('people'):
	os.makedirs('people')

os.chdir('people')
for i in os.listdir():
	name = os.path.splitext(i)[0]
	img = fr.load_image_file(i)
	encode = fr.face_encodings(img)[0]
	people.append({"name": name, "encode": encode})

os.chdir(curDir)

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


def snapshot(img):
	now = datetime.datetime.now()
	timestamp = str(int(datetime.datetime.timestamp(now)))
	# path = os.path.join("C:\\", "Users", uname,
	# 					"Desktop", "admin", timestamp + '.jpg')
	cv.imwrite("./people/" + timestamp + '.jpg', img)


def faceClassify(img):
	try:
		img = fr.face_encodings(img)[0]
	except:
		return "isUnknown"
	for profile in people:
		result = fr.compare_faces([profile["encode"]], img)
		if result[0]:
			if profile["name"] == 'admin':
				return "isAdmin"

	return "isUnknown"


def face():
	showFace = True
	showUB = showEye = recordVid = False

	cap = cv.VideoCapture(0, cv.CAP_DSHOW)
	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))

	size = (frame_width, frame_height)
	vid = cv.VideoWriter(
		'filename.avi', cv.VideoWriter_fourcc(*'MJPG'), 14, size)

	while True:
		_, img = cap.read()

		gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

		if showFace:
			faces = cascadeFace.detectMultiScale(gray, 1.1, 4)
			for x, y, w, h in faces:
				# cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 200), 4)

				identFace = faceClassify(img[y:y+h, x:x+w])
				try:
					if identFace == "isAdmin":
						temp = cv.resize(adminOverlay, (w+70, h+70))
						img = cvz.overlayPNG(img, temp, [x-35, y-35])
					elif identFace == "isThreat":
						temp = cv.resize(threatOverlay, (w+70, h+70))
						img = cvz.overlayPNG(img, temp, [x-35, y-10])
					elif identFace == "isFam":
						temp = cv.resize(famOverlay, (w+70, h+70))
						img = cvz.overlayPNG(img, temp, [x-35, y-35])
					elif identFace == "isUnknown":
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

		if len(faces) and recordVid:
			vid.write(img)

		cv.imshow('AI6', img)

		key = cv.waitKey(1)
		if key != -1:
			key = key & 0xff
			if key in (ord('q'), ord('Q')):
				break
			elif key in (ord('e'), ord('E')):
				showEye = not showEye
			elif key in (ord('f'), ord('F')):
				showFace = not showFace
			elif key in (ord('b'), ord('B')):
				showUB = not showUB
			elif key in (ord('c'), ord('C')):
				snapshot(img)
			elif key in (ord('r'), ord('R')):
				recordVid = not recordVid

	cap.release()
	vid.release()
	cv.destroyAllWindows()


if __name__ == '__main__':
	face()
