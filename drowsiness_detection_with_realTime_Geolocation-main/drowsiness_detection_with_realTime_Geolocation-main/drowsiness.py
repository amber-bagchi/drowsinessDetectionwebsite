import cv2
import os
from keras.models import load_model
import numpy as np
from pygame import mixer
import time
from geopy.geocoders import Nominatim
from twilio.rest import Client



mixer.init()
sound = mixer.Sound('AirHornR.wav')

face = cv2.CascadeClassifier('C:/Users/ANIMESH/Downloads/drowsiness_detection_with_realTime_Geolocation-main/drowsiness_detection_with_realTime_Geolocation-main/Trash/haarcascade_frontalface_alt.xml')
leye = cv2.CascadeClassifier('C:/Users/ANIMESH/Downloads/drowsiness_detection_with_realTime_Geolocation-main/drowsiness_detection_with_realTime_Geolocation-main/Trash/haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier('C:/Users/ANIMESH/Downloads/drowsiness_detection_with_realTime_Geolocation-main/drowsiness_detection_with_realTime_Geolocation-main/Trash/haarcascade_righteye_2splits.xml')



lbl=['Close','Open']

model = load_model('C:/Users/ANIMESH/Downloads/drowsiness_detection_with_realTime_Geolocation-main/drowsiness_detection_with_realTime_Geolocation-main/models/cnnCat2.h5')
path = os.getcwd()
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
count=0
score=0
thicc=2
rpred=[99]
lpred=[99]

while (True):
    ret, frame = cap.read()
    height, width = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(150, 150))
    left_eye = leye.detectMultiScale(gray)
    right_eye = reye.detectMultiScale(gray)

    cv2.rectangle(frame, (0, height - 50), (450, height), (0, 0, 0), thickness=cv2.FILLED)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)

    for (x, y, w, h) in right_eye:
        r_eye = frame[y:y + h, x:x + w]
        count = count + 1
        r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
        r_eye = cv2.resize(r_eye, (24, 24))
        r_eye = r_eye / 255
        r_eye = r_eye.reshape(24, 24, -1)
        r_eye = np.expand_dims(r_eye, axis=0)
        predict_x = model.predict(r_eye)
        rpred = np.argmax(predict_x, axis=1)
        if (rpred[0] == 1):
            lbl = 'Open'
        if (rpred[0] == 0):
            lbl = 'Closed'
        break

    for (x, y, w, h) in left_eye:
        l_eye = frame[y:y + h, x:x + w]
        count = count + 1
        l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
        l_eye = cv2.resize(l_eye, (24, 24))
        l_eye = l_eye / 255
        l_eye = l_eye.reshape(24, 24, -1)
        l_eye = np.expand_dims(l_eye, axis=0)
        predict_y = model.predict(l_eye)
        lpred = np.argmax(predict_y, axis=1)
        if (lpred[0] == 1):
            lbl = 'Open'
        if (lpred[0] == 0):
            lbl = 'Closed'
        break

    if (rpred[0] == 0 and lpred[0] == 0):
        score = score + 1
        cv2.putText(frame, "Closed", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    # if(rpred[0]==1 or lpred[0]==1):
    else:
        if (score > 20):
            score = score - 5
            cv2.putText(frame, "Open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        else:
            score = score - 2
            cv2.putText(frame, "Open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

    if (score < 0):
        score = 0
    cv2.putText(frame, 'Risk%:' + str(score), (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, 'Kosish', (220, height - 20), font, 1, (255, 0, 0), 1, cv2.LINE_AA)
    if (score > 8):
        # person is feeling sleepy so we beep the alarm
        cv2.imwrite(os.path.join(path, 'image.jpg'), frame)
        cv2.putText(frame, '!!Drowsiness Detected!!', (100, height - 80), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        try:
            sound.play()

        except:  # isplaying = False
            pass
        if (thicc < 2):
            thicc = thicc + 2
        else:
            thicc = thicc - 2
            if (thicc < 2):
                thicc = 2
        cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)
    cv2.imshow('frame', frame)
    # if score > 100 driver response 0
    if (score > 50):

        # # Create a Nominatim geolocator
        # geolocator = Nominatim(user_agent="my_location_app")

        # # Get your own IP address (you can use other methods to obtain coordinates)
        # my_ip = "2401:4900:1ca8:361c:88bd:eb46:3fe8:378e"
        # location = geolocator.reverse(my_ip)

        # # Print the location information
        # print("Your Location:")
        # print("Address:", location.address)
        # print("Latitude:", location.latitude)
        # print("Longitude:", location.longitude)

        # location scrapping
        geoloc = Nominatim(user_agent="GetLoc")
        loc_name = geoloc.reverse("23.334768320313177, 85.25905002811443")
        locations = loc_name.address
        # location conversion
        # sms sending
        account_sid = 'AC7d7779b5eb371fdad4a5ce8091506db7'
        auth_token = 'adb91b2306c642e30f5a6304659614cf'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='+18454787512',
            body='Drowsiness Detected !! My current location is :-  Amity University Ranchi, ' + str(locations),
            to='+917903301466'
        )
        print(message.sid)
        # sms sending ends
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()