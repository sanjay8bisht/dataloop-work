import os
import cv2


def detect(path,img):
    cascade = cv2.CascadeClassifier(path)

    img=cv2.imread(img,1)
    # converting to gray image for faster video processing
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = cascade.detectMultiScale(img_gray, 1.3, 5)
    print(faces)
    # if at least 1 face detected
    if len(faces) > 0:
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            print(x, y, x+h, y+w)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        # Display the resulting frame
        cv2.imshow('Face Detection', img)
        # wait for 'c' to close the application
        cv2.waitKey(0)


def main():
    cascadeFilePath = "haarcascade_frontalface_default.xml"
    print(cascadeFilePath)
    img='/Users/meena392/Downloads/human_faces/male/face1.jpg'
    detect(cascadeFilePath,img)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()