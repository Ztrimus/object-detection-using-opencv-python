import cv2
class Shapedetector:
    def __init__(self):
        pass
    def detect(self,c):
        shape="Unidentified"
        peri=cv2.arcLength(c,True)
        approx=cv2.approxPolyDP(c,0.04*peri,True)
        if len(approx)==3:
            shape="Triangle"
        elif len(approx)==4:
            (x,y,w,h)=cv2.boundingRect(approx)
            ar=w/ float(h)
            shape = "Square" if ar >= 0.95 and ar <= 1.05 else "Rectangle"
            
        else:
            shape = "Circle"
        return shape
