
import tensorflow as tf
from tensorflow import keras
import serial
import numpy as np
import cv2
print('serial ' + serial.__version__)

# Set a PORT Number & baud rate
PORT = 'COM6'
BaudRate = 9600

ard= serial.Serial(PORT,BaudRate)

emotion =  ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def led_on():
    ard.write(b'1')
    print('on')
def led_off():
    ard.write(b'0')
    print('off')

model = keras.models.load_model("traindModel.h5")
font = cv2.FONT_HERSHEY_SIMPLEX
cam = cv2.VideoCapture(0)
face_cas = cv2.CascadeClassifier('front_face.xml')
i=0
totalemotion = []
while True:
    ret, frame = cam.read()
    
    if ret==True:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cas.detectMultiScale(img, 1.3,5)
        
        for (x, y, w, h) in faces:
            face_component = img[y:y+h, x:x+w]
            fc = cv2.resize(face_component, (48, 48))
            inp = np.reshape(fc,(1,48,48,1)).astype(np.float32)
            inp = inp/255.
            prediction = model.predict_proba(inp)
            em = emotion[np.argmax(prediction)]
            i = i + 1
            totalemotion.append(em)
            score = np.max(prediction)
            cv2.putText(frame, em+"  "+str(score*100)+'%', (x, y), font, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)


            if em == 'Happy':
                if totalemotion[i-2] != 'Happy':
                    led_on()

            elif em == 'Disgust':
                if totalemotion[i - 2] != 'Disgust':
                    led_off()

            elif em == 'Anger':
                if totalemotion[i - 2] != 'Anger':
                    led_off()

        cv2.imshow("image", frame)
        
        if cv2.waitKey(1) == 27:
            break
    else:
        print ('Error Detected')

cam.release()
cv2.destroyAllWindows()
