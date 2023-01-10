import os
import dtlpy as dl
import cv2


class ServiceRunner(dl.BaseServiceRunner):

    def __init__(self) -> None:
        print('-----', cv2.__version__)
        self.artifacts_package_name = 'gender-classification-3'
        self.package = dl.packages.get(package_name=self.artifacts_package_name)
        self.faceProto = "opencv_face_detector.pbtxt"
        self.faceModel = "opencv_face_detector_uint8.pb"
        self.genderProto = "gender_deploy.prototxt"
        self.genderModel = "gender_net.caffemodel"
        self.frontalFaceCasscade = 'haarcascade_frontalface_default.xml'
        self.full_faceProto_path = os.path.join(os.getcwd(), 'artifacts', self.faceProto)
        self.full_faceModel_path = os.path.join(os.getcwd(), 'artifacts', self.faceModel)
        self.full_genderProto_path = os.path.join(os.getcwd(), 'artifacts', self.genderProto)
        self.full_genderModel_path = os.path.join(os.getcwd(), 'artifacts', self.genderModel)
        self.full_frontalFaceCasscade_path = os.path.join(os.getcwd(), 'artifacts', self.frontalFaceCasscade)
        self.download_artifacts()
        self.face_cascade = cv2.CascadeClassifier(self.full_frontalFaceCasscade_path)

    def download_artifacts(self):
        print(self.full_faceProto_path, self.full_faceModel_path)
        print('artifacts', self.package.artifacts.list().print())
        if not os.path.isfile(self.full_faceProto_path):
            self.package.artifacts.download(artifact_name=self.faceModel,
                                            local_path=self.full_faceProto_path)
        if not os.path.isfile(self.full_faceModel_path):
            self.package.artifacts.download(artifact_name=self.faceModel,
                                            local_path=self.full_faceModel_path)
        if not os.path.isfile(self.full_genderProto_path):
            self.package.artifacts.download(artifact_name=self.genderProto,
                                            local_path=self.full_genderProto_path)
        if not os.path.isfile(self.full_genderModel_path):
            self.package.artifacts.download(artifact_name=self.genderModel,
                                            local_path=self.full_genderModel_path)
        if not os.path.isfile(self.full_frontalFaceCasscade_path):
            self.package.artifacts.download(artifact_name=self.frontalFaceCasscade,
                                            local_path=self.full_frontalFaceCasscade_path)

    @staticmethod
    def getFaceBox(net, frame, conf_threshold=0.75):
        print(f"frame, {frame}")
        frameOpencvDnn = frame.copy()
        frameHeight = frameOpencvDnn.shape[0]
        frameWidth = frameOpencvDnn.shape[1]
        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300),
                                     [104, 117, 123], True, False)

        print("blob", blob)

        net.setInput(blob)
        detections = net.forward()
        print(f"detections {detections}")
        bboxes = []

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            print("confidence", confidence, "conf_threshold", conf_threshold)
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                bboxes.append([x1, y1, x2, y2])
                cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0),
                              int(round(frameHeight / 150)), 8)

        return frameOpencvDnn, bboxes

    def gender_classification(self, item: dl.Item):
        print("[INFO] downloading image...")
        filename = item.download()
        print(f"filename {filename}")
        try:

            MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
            genderList = ['Male', 'Female']
            padding = 0

            # load the network
            genderNet = cv2.dnn.readNet(self.full_genderModel_path, self.full_genderProto_path)
            faceNet = cv2.dnn.readNet(self.full_faceModel_path, self.full_faceProto_path)

            print('genderNet', genderNet)

            img = cv2.imread(filename)

            print(f"image {img}")

            small_frame = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

            _, bboxes = self.getFaceBox(faceNet, img)
            print(f"bboxes {bboxes}")

            for bbox in bboxes:
                print(bbox, len(img), len(img[0]))
                face = img[max(0, bbox[1] - padding):min(bbox[3] + padding, img.shape[0] - 1),
                       max(0, bbox[0] - padding):min(bbox[2] + padding, img.shape[1] - 1)]
                print(face)
                blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                genderNet.setInput(blob)
                genderPreds = genderNet.forward()
                gender = genderList[genderPreds[0].argmax()]
                print("Gender : {}, conf = {:.3f}".format(gender, genderPreds[0].max()))

                builder = item.annotations.builder()
                builder.add(annotation_definition=dl.Classification(label=gender))
                item.annotations.upload(builder)

                if genderPreds[0].max() > 0.5:
                    builder.add(
                        annotation_definition=dl.Box(
                            top=bbox[1],
                            left=bbox[0],
                            right=bbox[2],
                            bottom=bbox[3],
                            label=gender
                        ),
                        model_info={
                            'name': 'Caffe',
                            'confidence': genderPreds[0].max()
                        }
                    )
                    item.annotations.upload(builder)
            return item
        except:
            os.remove(filename)

    def face_detection(self, item: dl.Item):
        print("[INFO] downloading image...")
        filename = item.download()
        print(f"filename {filename}")
        try:

            img = cv2.imread(filename)

            print(f"image {img}")

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(img_gray, 1.3, 5)

            print(f'faces {faces}')

            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    print(x, y, x + h, y + w)
                    builder = item.annotations.builder()
                    builder.add(
                        annotation_definition=dl.Box(
                            top=y,
                            left=x,
                            right=x + w,
                            bottom=y + h,
                            label="face"
                        )
                    )
                    item.annotations.upload(builder)

            return item
        except:
            os.remove(filename)
