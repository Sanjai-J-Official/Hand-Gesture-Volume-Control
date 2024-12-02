import time
import cv2



class fpscls:
    def __inti__(self):
        pass
         

    
    def fpsFun(self,img,fps):

        cv2.putText(img,str(int(fps)),(10,40),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
        cv2.imshow('Img',img)
        return img
    


cls=fpscls()      
def main():
    ptime=0
    cap=cv2.VideoCapture(0)
    
    
    while True:
        istrue ,img=cap.read()

        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        img=cls.fpsFun(img,fps)

     
        
  

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        


if __name__=="__main__":
    main()

