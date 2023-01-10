import os
import cv2

def getFaceBox(net, frame,conf_threshold = 0.75):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn,1.0,(300,300),
                                 [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []

    for i in range(detections.shape[2]):
        confidence = detections[0,0,i,2]
        if confidence > conf_threshold:
            x1 = int(detections[0,0,i,3]* frameWidth)
            y1 = int(detections[0,0,i,4]* frameHeight)
            x2 = int(detections[0,0,i,5]* frameWidth)
            y2 = int(detections[0,0,i,6]* frameHeight)
            bboxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn,(x1,y1),(x2,y2),(0,255,0),
                          int(round(frameHeight/150)),8)

    return frameOpencvDnn , bboxes

faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"

# ageProto = "age_deploy.prototxt"
# ageModel = "age_net.caffemodel"

genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']
padding = 20

#load the network
# ageNet = cv2.dnn.readNet(ageModel,ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)
faceNet = cv2.dnn.readNet(faceModel, faceProto)

img='/Users/meena392/Downloads/human_faces/female/face1.jpg'
img=cv2.imread(img,1)

small_frame = cv2.resize(img,(0,0),fx = 0.5,fy = 0.5)

frameFace ,bboxes = getFaceBox(faceNet, small_frame)

for bbox in bboxes:
    print(bbox, len(small_frame), len(small_frame[0]))
    face = small_frame[max(0,bbox[1]-padding):min(bbox[3]+padding,img.shape[0]-1),
            max(0,bbox[0]-padding):min(bbox[2]+padding, img.shape[1]-1)]
    print(face)
    blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
    genderNet.setInput(blob)
    genderPreds = genderNet.forward()
    gender = genderList[genderPreds[0].argmax()]
    print("Gender : {}, conf = {:.3f}".format(gender, genderPreds[0].max()))