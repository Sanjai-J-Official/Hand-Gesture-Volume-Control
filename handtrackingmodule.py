import time
import cv2
import mediapipe as mp

class handDetetor():
    def __init__(self,mode=False,maxHands=2,detectconf=0.90,trackconf=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectconf=detectconf
        self.trackconf=trackconf

        self.mphands=mp.solutions.hands
        self.hands = self.mphands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectconf,
            min_tracking_confidence=self.trackconf,
        )

        self.mpdraws=mp.solutions.drawing_utils 

    def findHands(self,imgf,draw=True):
        imgrgb=cv2.cvtColor(imgf,cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(imgrgb)

        if self.result.multi_hand_landmarks:
            for handLMS in self.result.multi_hand_landmarks:
                if draw:
                
                    self.mpdraws.draw_landmarks(imgf,handLMS,self.mphands.HAND_CONNECTIONS)
        return imgf
    
    def findposition(self,img,draw=True):
        list_lm=[]
        if self.result.multi_hand_landmarks:
            for handLMS in self.result.multi_hand_landmarks:
                for (id,lms) in enumerate(handLMS.landmark):
                    h,w=img.shape[:2]
                    cx,cy=int(lms.x*w),int(lms.y*h)
                    
                    # print(id,cx,cy)
                    

                #if id==handno:
                    list_lm.append([id,cx,cy])
                    
                    #if draw:
                        #cv2.circle(img,(cx,cy),25,(0,90,255),cv2.FILLED)
        return list_lm


  



   
def main():
    ptime=0
    ctime=0
    cap=cv2.VideoCapture(0)
    detector=handDetetor()
    
    while True:
        istrue ,imgf=cap.read()
        img=cv2.flip(imgf,1)
        img = detector.findHands(img,draw=False)
        listlms=detector.findposition(img,8)
        if len(listlms) !=0:
            print(listlms)
        

        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
        cv2.imshow('Img',img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        
        
if __name__=="__main__":
    main()