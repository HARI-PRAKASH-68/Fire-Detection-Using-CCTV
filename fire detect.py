import threading
import cv2
import playsound as pl
import time
import dlib
video = cv2.VideoCapture(0)
fire_cascade = cv2.CascadeClassifier('cascadefile')
runOnce = False
def play_alarm_sound_function():
    pl.playsound('alarmsound', True)
detector = dlib.get_frontal_face_detector()
video.set(3, 640)
video.set(4, 480)
width = video.get(3)
height = video.get(4)
print("video resolution is set to ", width, 'X', height)
print("Help -->\nPress esc key to Exit")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
date_time = time.strftime("Recordings %d-%m-%y %H-%M")
output = cv2.VideoWriter('footages/'+date_time+'.mp4', fourcc, 20.0, (640, 480))
while video.isOpened():
    Alarm_Status = False
    check, frame = video.read()
    if check == True:
        frame = cv2.flip(frame, 1)
        t = time.ctime()
        fire = fire_cascade.detectMultiScale(frame, 1.2, 5)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        cv2.rectangle(frame, (5, 5, 100, 20), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, "Camera1", (20, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (5, 5, 5), 1)
        cv2.putText(frame, t, (420, 460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (5, 5, 5), 2)
        i = 0
        for face in faces:
            x, y = face.left(), face.top()
            x1, y1 = face.right(), face.bottom()
            cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
            i = i + 1
            cv2.putText(frame, 'face num'+str(i), (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        for (x2, y2, w1, h1) in fire:
            cv2.rectangle(frame, (x2-20, y2-20), (x2+w1+20, y2+h1+20), (255, 0, 0), 2)
            roi_gray=gray[y2:y2+h1, x2:x2+w1]
            roi_color = frame[y2:y2+h1, x2:x2+w1]
            if runOnce == False:
                print("FIRE DETECT")
                runOnce = False
                threading.Thread(target = play_alarm_sound_function ).start()
        cv2.imshow('CCTV CAMERA', frame)
        output.write(frame)
        if cv2.waitKey(1) == 27:
            print("Video footage saved")
            break
    else:
        print("Can't open Camera")
        break
video.release()
output.release()
cv2.destroyAllWindows()
