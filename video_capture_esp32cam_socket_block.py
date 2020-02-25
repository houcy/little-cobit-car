import cv2 as cv
import numpy as np
import urllib.request
import socket

stream=urllib.request.urlopen("http://192.168.0.15:81/stream")
bts=b''
              
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect(("192.168.0.15", 82))

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

while True: 
    bts+=stream.read(4096)
    jpghead=bts.find(b'\xff\xd8')
    jpgend=bts.find(b'\xff\xd9')
    if jpghead>-1 and jpgend>-1:
        jpg=bts[jpghead:jpgend+2]
        bts=bts[jpgend+2:]
        buff = np.frombuffer(jpg,dtype=np.uint8)
        if buff.any():
            img=cv.imdecode(buff,cv.IMREAD_UNCHANGED)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for i in faces:
                print("stop")
                message = b'stop\n'
                #sock.sendall(message)
                cv.rectangle(img, (i[0], i[1]), (i[0]+i[2], i[1]+i[3]), (255, 0, 0), 2)
            cv.imshow("a",img)
    k=cv.waitKey(1)
    if k & 0xFF==ord('q'):
        break
   
cv.destroyAllWindows()