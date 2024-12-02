import cv2
import mediapipe as mp
import numpy as np
import handtrackingmodule as htm
import fps
import time
import math 
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()

volrange=volume.GetVolumeRange()

minvol=volrange[0]
maxvol=volrange[1]




############################################

wcam,hcam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)

detector=htm.handDetetor()
fpsclass=fps.fpscls()
ptime=0
volBar=400
volPer=0
while True:
    success,img=cap.read()

    if not success:
        break

    img=detector.findHands(img)
    listlms=detector.findposition(img)

    if len(listlms)!=0:
       # print(listlms[4],listlms[8])

        x1,y1=listlms[4][1],listlms[4][2]
        x2,y2=listlms[8][1],listlms[8][2]

        cv2.circle(img,(x1,y1),12,(25,144,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),12,(25,144,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(25,144,0),3)
        cx,cy=(x2+x1)//2,(y2+y1)//2
        cv2.circle(img,(cx,cy),12,(25,144,0),cv2.FILLED)

        


        length=math.hypot(x2-x1,y2-y1)
        
        if length<50:
            cv2.circle(img,(cx,cy),12,(0,0,250),cv2.FILLED)

        vol=np.interp(length,[30,250],[minvol,maxvol])
        volBar=np.interp(length,[30,250],[400,150])
        volPer=np.interp(length,[30,250],[0,100])
        volume.SetMasterVolumeLevel(vol, None)

        
    
    cv2.rectangle(img,(50,150),(85,400),(255,0,0))
    
    cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)

    cv2.putText(img,str(f"{int(volPer)}%"),(40,450),cv2.FONT_HERSHEY_PLAIN,2.5,(255,0,0),3)
    

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    
    img=fpsclass.fpsFun(img,fps)
    cv2.imshow("img",img)
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break
 
