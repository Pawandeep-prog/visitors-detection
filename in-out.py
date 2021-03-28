import cv2
import numpy as np

cap = cv2.VideoCapture(0)

_, frame1 = cap.read()

left, center, right = False, False, False
x=300

mask = np.zeros((200, 400))
while True:

	_, frame2 = cap.read()

	g1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
	g2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

	diff = cv2.absdiff(g1, g2)

	_, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

	contr, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	if len(contr) > 0:
		contr = max(contr, key=cv2.contourArea)
		x,y,w,h = cv2.boundingRect(contr)
		cv2.rectangle(frame2, (x,y), (x+w, y+h), (0,255,0), 2)

	if not(left) and not(right):
		if x < 100:
			left = True

		elif x > 500:
			right = True

	elif left : 
		if x < 450 and x > 200 and not(center):
			print(x," x has been set to it")
			center = True

		elif x > 500:
			if center:
				print("motion to left taken place")
				mask = np.zeros((200, 400))
				cv2.putText(mask, "to left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255), 3)
				left = False
				center = False
			else:
				right = True

	elif right : 
		if x < 450 and x > 200 and not(center):
			print(x," x has been set to it")
			center = True
		if x < 100:
			if center:
				print("motion done to the right side")
				mask = np.zeros((200, 400))
				cv2.putText(mask, "to right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255), 3)
				right = False
				center = False

			else:
				left = True

	cv2.imshow("window", thresh)
	cv2.imshow("window2", frame2)
	cv2.imshow("mask", mask)

	_, frame1 = cap.read()

	if cv2.waitKey(1) == 27:
		cv2.destroyAllWindows()
		cap.release()
		break