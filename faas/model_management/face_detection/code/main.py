import cv2
import numpy

model = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'weights.caffemodel')


# batch is an array

img = '/Users/meena392/Downloads/human_faces/male/face3.jpg'
# read the image using cv2
image = cv2.imread(img)
# accessing the image.shape tuple and taking the elements
(h, w) = image.shape[:2]
# get our blob which is our input image
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
# input the blob into the model and get back the detections
model.setInput(blob)
detections = model.forward()
count = 0
for i in range(0, detections.shape[2]):
    box = detections[0, 0, i, 3:7] * numpy.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")
    confidence = detections[0, 0, i, 2]
    if confidence > 0.5:
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
        count = count + 1
# save the modified image to the Output folder
cv2.imshow("output", image)
cv2.waitKey(0)

# return a list of dl annotation collection (dl.AnnotationCollection/dl.)
