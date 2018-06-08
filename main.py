#classes and subclasses to import
from Shapedetector import Shapedetector
from Colordetector import Colordetector
#from Counting import Counting
import cv2
import numpy as np
import os

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write rerults to a csv
def writecsv(color,shape,size,count):
                #open csv file in append mode
                filep = open('resultsCSV.csv','a')
                # create string data to write per image
                datastr = "," + color + "-" + shape + "-" + size + "-" + count
                #write to csv
                filep.write(datastr)
                filep.close()

def sizeDetector(area, shape):
                        #Detecting size of Circle
                        if shape == "Circle" :
                                        if area <= 2407:
                                            return "Small"
                                        elif area >= 8747:
                                            return 'Large'
                                        else:
                                            return 'Medium'

                        #Detecting size of Square
                        if shape == "Square" :
                                        if area <= 3023:
                                            return "Small"
                                        elif area >= 11017:
                                            return 'Large'
                                        else:
                                            return 'Medium'

                        #Detecting size of Rectangle
                        if shape == "Rectangle" :
                                        if area <= 3621:
                                            return "Small"
                                        elif area >= 21517:
                                            return 'Large'
                                        else:
                                            return 'Medium'

                        #Detecting size of Triangle
                        if shape == "Triangle" :
                                        if area <= 1686:
                                            return "Small"
                                        elif area >= 5969.5:
                                            return 'Large'
                                        else:
                                            return 'Medium'

class Counting:
                    counted=0
                    #Initialize the "Counting" class
                    def __init__(self,shape,color,size):
                                self.shape = shape
                                self.color = color
                                self.size = size  


#counted=0    
def main(path):
#####################################################################################################
    #Write your code here!!!
#####################################################################################################
                #Received image from given path
                img_no = path
                #load the image
                image = cv2.imread(img_no)
                #Detecting edges in image
                edges = cv2.Canny(image,100,100)
                #the L*a*b* color spaces
                lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                #thresholding it to reveal the shapes in the image
                ret,thresh = cv2.threshold(edges, 230, 255, cv2.THRESH_BINARY)

                # find contours in the thresholded image
                _, cnts, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

                # initialize the shape detector and color labeler
                SD = Shapedetector() 
                CD = Colordetector()
                count1 = []
                array=[]
                # loop over the contours
                for c in cnts:
                                    # compute the co-ordinates of the contour
                                    x,y,w,h = cv2.boundingRect(c)
                                    area = cv2.contourArea(c)
                                    # detect the shape of the contour
                                    shape = SD.detect(c)
                                    # label the color to contour
                                    color = CD.label(lab, c)
                                    #Finding Size of contour
                                    size = sizeDetector(area,shape)
                                    s=Counting(shape,color,size)
                                    count1.append(s)
                                    text = "{}-{}-{}".format(color,shape,size)
                                     #draw the contours 
                                    cv2.drawContours(image, [c], -1, (0, 0, 0), 2)
                                    #giving name of the shape and color on the image
                                    cv2.putText(image, text, (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
                                    # show the output image
                                    cv2.imshow("Image", image)
                                    #waiting to press any to detect next contour
                                    cv2.waitKey(0)

                #counting total object of given image    
                n=len(count1)
                #total object of given image
                m=n/2
                i=0
                while(i<m):
                                array.append(count1[2*i])
                                i=i+1
         
                m=len(array)
                k=0
                j=0
                currentImg = img_no.split("\\")
                #print total number object
                print "Total number of object in ", currentImg[1] , " is  = ",str(m) 

                for k in range(m):
                                if( array[k].counted==0):
                                                count=1
                                                j=k+1
                                                while(j<m):
                                                            if array[k].shape==array[j].shape and array[k].color==array[j].color and array[k].size==array[j].size and array[j].counted==0:
                                                                array[j].counted=1
                                                                count=count+1
                                                            j=j+1  
                                                writecsv(array[k].color,array[k].shape,array[k].size,str(count))
                                                TEXT = "{}-{}-{}-{}".format(array[k].color,array[k].shape,array[k].size,str(count))
                                                print TEXT

                #Destroying all displaying windows
                cv2.destroyAllWindows()
print "=============================================================================="
print "             !!! PRESS ANY KEY TO CHECK NEXT OBJECT'S CONTOUR, SHAPE, COLOR. !!!"
print "=============================================================================="
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
   #main where the path is set for the directory containing the test images
if __name__ == "__main__":
    mypath = '.'
    #getting all files in the directory
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if f.endswith(".PNG")]
    #iterate over each file in the directory
    for fp in onlyfiles:
        #Open the csv to write in append mode
        filep = open('resultsCSV.csv','a')
        #this csv will later be used to save processed data, thus write the file name of the image
        data = fp.split("\\")
        print ""
        print data[1]
        print "==========="
        #We replace this  "filep.write(fp)"
        filep.write(data[1])
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open('resultsCSV.csv','a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
        print "\n"
