import cv2

# Initialize the video capture object
cam = cv2.VideoCapture("C:/Users/pc/Downloads/mocap.mp4")

# Initialize the object tracker using MOSSE algorithm
#track = cv2.legacy.TrackerMOSSE_create()
track = cv2.legacy.TrackerCSRT_create()
# Read the first frame from the video stream
sucess, img = cam.read()

# Select the object to track using a bounding box
box = cv2.selectROI("Tracker",img,False)

# Initialize the tracker with the selected bounding box
track.init(img,box)

# Define a function to draw a bounding box around the tracked object
def drawBOX(img,box):
    x,y,w,h = int(box[0]),int(box[1]),int(box[2]),int(box[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(0,255,0),3,1)
    cv2.putText(img,"found",(20,105),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2)#green

# Start the main loop
while True:
       
    # Get the current time
    ct = cv2.getTickCount()

    # Read a frame from the video stream
    sucess,img = cam.read()

    # Update the tracker with the new frame
    sucess,box = track.update(img) 

    if sucess:
       # Draw a bounding box around the tracked object
       drawBOX(img,box)

       # Crop the image to only show the tracked object
       x,y,w,h = box
       imgcrop = img[int(y):int(y+h), int(x):int(x+w)]

    else:
       # If the object is lost, display a red text
       cv2.putText(img,"lost",(20,105),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),2)#red

    # Calculate the frame per second (FPS) of the video stream
    fps = cv2.getTickFrequency()/(cv2.getTickCount()-ct)

    # Display the FPS and the tracked image
    cv2.putText(img,f'FPS: {int(fps)}',(20,70),cv2.FONT_HERSHEY_PLAIN,3,(0, 255,0),2)#green
    cv2.imshow("Image",img)

    if sucess:
       # Display the cropped image
       x,y,w,h = box
       imgcrop = img[int(y):int(y+h), int(x):int(x+w)]
       cv2.imshow("CropedImage",imgcrop)
    
    # Quit the program if 'q' is pressed
    if cv2.waitKey(10) & 0xff == ord('w'):
        break
