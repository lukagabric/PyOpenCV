'''

    A demonstration for face and object detection using haar-like features.
    Faces are found in a video stream and a red box is drawn around them.
    
    Because of a bug in OpenCV on Mac OS X, the camera window may not close
    after the program is ended, in which case you will need to
    "Force Quit" Python.

Modified (30 July 2011) by Donald J. Woodbury
                            and David C. Bailey (dbailey@physics.utoronto.ca)
    from the example by Jo Vermeulen retrieved from
        http://blog.jozilla.net/2008/06/27/fun-with-python-opencv-and-face-detection/,
        (License: Not known)
    which in turn is based on a script by Nirav Patel from
        http://eclecti.cc/olpc/face-detection-on-the-olpc-xo
        (License: http://creativecommons.org/licenses/by/3.0/us/)
    which is derived from the facedetect.py example by Roman Stanchak & James Bowman,
         available from http://sourceforge.net/projects/opencvlibrary/.
    OpenCV is available under the BSD License (http://opencv.willowgarage.com/wiki/).
    The modifications by Woodbury and Bailey are released
        under the MIT License - http://www.opensource.org/licenses/mit-license.php.

    '''

import sys
import cv2.cv as cv

def detect_and_draw(image):
    image_size = cv.GetSize(image)
 
    # convert color input image to grayscale
    grayscale = cv.CreateImage(image_size, 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
 
    # create storage
    storage = cv.CreateMemStorage(0)
 
    # equalize histogram
    cv.EqualizeHist(grayscale, grayscale)
 
    # detect objects
    
    # locate relevant haar cascade data
    haarlocation = '/Users/lukagabric/Workspaces/Kepler/Workspaces/PyOpenCV/haarcascade_frontalface_alt.xml' # Mac OS X example
    
    # load haar cascade data
    cascade = cv.Load(haarlocation)
    faces = cv.HaarDetectObjects(grayscale, cascade, storage, 1.2, 2,
                                    cv.CV_HAAR_DO_CANNY_PRUNING, (100, 100))
 
    if faces:
        print 'face detected!    Press Escape to exit program.'
        for i in faces:
            cv.Rectangle(image, (int(i[0][2])+int(i[0][0]), int(i[0][3])+int(i[0][1])),
                                    (int(i[0][0]), int(i[0][1])), (0, 255, 0), 3, 8, 0)
 
if __name__ == "__main__":
 
    print "Press ESC to exit ..."
 
    # create windows
    cv.NamedWindow('Camera', cv.CV_WINDOW_AUTOSIZE)
 
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
 
        # face detection
        detect_and_draw(frame)
 
        # display webcam image
        cv.ShowImage('Camera', frame)
 
        # handle events
        #    As long as camera window has focus (e.g. is selected), this will intercept
        #        pressed key; it will not work if the python terminal window has focus
        k = cv.WaitKey(100)
         
        if k == 0x1b: # ESC
            print 'ESC pressed. Exiting ...'
            cv.DestroyWindow("Camera")  # This may not work on a Mac
            break