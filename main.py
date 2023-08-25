import cv2 as cv


 
# initialize the camera
# If you have multiple camera connected with 
# current device, assign a value in cam_port 
# variable according to that
cam_port = 0
cam = cv.VideoCapture(cam_port)
  
# reading the input using the camera
result, image = cam.read()
  
# If image will detected without any error, 
# show result
if result:
    
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, (7,6), None)

if ret == True:
    image = cv.drawChessboardCorners(image, (7,6), corners, ret)


    # showing result, it take frame name and image 
    # output
    cv.imshow("capture", image)
    cv.imshow("gray", gray)



    # saving image in local storage
    cv.imwrite("capture.png", image)
  
    # If keyboard interrupt occurs, destroy image 
    # window
    cv.waitKey(0)
    cv.destroyAllWindows
  
# If captured image is corrupted, moving to else part
else:
    print("No image detected. Please! try again")