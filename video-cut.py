import cv2
import urllib
import http.client, urllib.request, urllib.parse, urllib.error
import matplotlib.pyplot as plt

cam = cv2.VideoCapture("video.mp4")

currentframe = 0
step = 1
frame_per_second = cam.get(cv2.CAP_PROP_FPS) 

while (True):

    ret, frame = cam.read()
    name = 'frame' + str(step) + '.jpg'
    
    if ret:
    
        if currentframe / (5*frame_per_second*step) > 1:  
          cv2.imwrite("videoFrames/" + name, frame)
          print("Videoframe " + str(step) + " is created")
          step+=1
          
          
        currentframe += 1
    else:
        break
    

cam.release()
cv2.destroyAllWindows()

#https://www.youtube.com/watch?v=d0yGdNEWdn0

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'f12693bc12c7479d829a57734f145e24',
}

params = urllib.parse.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'recognitionModel': 'recognition_03',
    'returnRecognitionModel': 'false',
    'detectionModel': 'detection_02',
})

for f in range(1, step):
    image_name = "frame" + str(f) + ".jpg"
    image = open("videoFrames/" + image_name, 'rb')
    top = 0
    left = 0
    width = 0
    height = 0

    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, image.read(), headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print(e)
        
    string = data.decode("utf-8")
    arr = string.split(',')
    if(len(arr)>1):
        top = int(arr[1][23:])
        left = int(arr[2][7:])
        width = int(arr[3][8:])
        height = int(arr[4][9:-3])
        #print(top, left, width, height)
       
        
        import numpy as np   
        img = cv2.imread("videoFrames/" + image_name)
        
        canva = np.zeros([img.shape[0]+300, img.shape[1]+320, 3]) 
        canva[150:-150, 160:-160] = img
    
        frame = canva[top:top+height+300, left:left+width+320]

        cv2.imwrite("faceFrames/changed_" + image_name, frame)
        print("Faceframe " + str(f) + " is created")

        
    
    
    
    
    
    
    