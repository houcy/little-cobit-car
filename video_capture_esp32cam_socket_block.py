import cv2 as cv
import numpy as np
import urllib.request
import socket
import serial

stream=urllib.request.urlopen("http://192.168.0.9:81/stream")
byte_array=b''
              
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect(("192.168.0.9", 82))

haar_class = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

ser 

while True: 
    data = sock.recv(1)
    print(data.decode())
    byte_array+=stream.read(4096)
    jpghead=byte_array.find(b'\xff\xd8')
    jpgend=byte_array.find(b'\xff\xd9')
    if jpghead>-1 and jpgend>-1:
        is_jpeg = True
    else:
        is_jpeg = False
    if is_jpeg:  
        jpg=byte_array[jpghead:jpgend+2]
        byte_array=byte_array[jpgend+2:]
        jpeg_img = np.frombuffer(jpg,dtype=np.uint8)
        is_OK = jpeg_img.any()
        if is_OK:
            img = cv.imdecode(jpeg_img,cv.IMREAD_UNCHANGED)
            img_cvt = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            detected_object = haar_class.detectMultiScale(img_cvt, 1.3, 5)
    
            for i in detected_object:
                message = b'stop\n'
                #sock.sendall(message)
                cv.rectangle(img, (i[0], i[1]), (i[0]+i[2], i[1]+i[3]), (255, 0, 0), 2)
       
            cv.imshow("a",img)
    k=cv.waitKey(1)
    if k & 0xFF==ord('q'):
        break
    
   
cv.destroyAllWindows()