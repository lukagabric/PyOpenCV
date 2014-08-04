import cv2
import cv2.cv as cv
import numpy as np
import sys
        
     
if __name__ == "__main__":
 
    print "Press ESC to exit ..."
 
    # create windows
    cv.NamedWindow('Original', cv.CV_WINDOW_AUTOSIZE)
    cv.NamedWindow('Threshold', cv.CV_WINDOW_AUTOSIZE)
 
    # create capture device
    capture = cv.CreateCameraCapture(0) # assume we want first device
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
 
    # check if capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit(1)
        
    while 1:
        # do forever
 
        #capture the current frame
        frame = cv.QueryFrame(capture)
        
        if frame is None:
            break
 
        # mirror
        cv.Flip(frame, None, 1)
        
        originalImage = frame
 
        hsvImage = cv.CreateImage(cv.GetSize(originalImage), 8, 3)
        cv.CvtColor(originalImage, hsvImage, cv.CV_BGR2HSV)
                            
        thresholdImage = cv.CreateImage(cv.GetSize(originalImage), 8, 1)
        cv.InRangeS(hsvImage, cv.Scalar(20.74, 75, 75), cv.Scalar(30.74, 255, 255), thresholdImage)
                                       
        thresholdImageArray = np.asarray(cv.GetMat(thresholdImage))
        thresholdImageArray = cv2.GaussianBlur(thresholdImageArray, (0,0), 2)

        thresholdImage = cv.fromarray(thresholdImageArray)
        
        circles = cv2.HoughCircles(thresholdImageArray,cv.CV_HOUGH_GRADIENT,2,10,param1=40,param2=80,minRadius=4,maxRadius=1500)
        
        if circles is not None:
            if circles.size > 0:
                circles = np.uint16(np.around(circles))
            
            for i in circles[0,:]:
                imageArray = np.asarray(cv.GetMat(originalImage))
                # draw the outer circle
                cv2.circle(imageArray,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(imageArray,(i[0],i[1]),2,(0,0,255),3)
                print "center = ", i[0], ",", i[1]
        
        # display webcam image
        cv.ShowImage('Original', originalImage)
        cv.ShowImage('Threshold', thresholdImage)
 
        # handle events
        #    As long as camera window has focus (e.g. is selected), this will intercept
        #        pressed key; it will not work if the python terminal window has focus
        k = cv.WaitKey(100)
         
        if k == 0x1b: # ESC
            print 'ESC pressed. Exiting ...'
            cv.DestroyWindow("Original")  # This may not work on a Mac
            cv.DestroyWindow("Threshold")  # This may not work on a Mac
            break