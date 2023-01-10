from abc import ABC

import dtlpy as dl
import os
import cv2
import numpy as np


@dl.Package.decorators.module(name='model-adapter',
                              description='Model Adapter for my model',
                              init_inputs={'model_entity': dl.Model})
class SimpleModelAdapter(dl.BaseModelAdapter, ABC):
    def load(self, local_path, **kwargs):
        print('loading a model')
        self.model = cv2.dnn.readNetFromCaffe(os.path.join(local_path, 'deploy.prototxt'),
                                              os.path.join(local_path, 'res10_300x300_ssd_iter_140000.caffemodel'))

    def predict(self, batch, **kwargs):
        print('predicting batch of size: {}'.format(len(batch)))
        batch_annotations = list()
        for image in batch:
            image_annotations = dl.AnnotationCollection()
            (h, w) = image.shape[:2]
            print(f'image width {w}, height {h}')
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            self.model.setInput(blob)
            detections = self.model.forward()
            for i in range(0, detections.shape[2]):
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    print(f'face detected with confidence {confidence}')
                    image_annotations.add(annotation_definition=dl.Box(left=float(startX),
                                                                       top=float(startY),
                                                                       right=float(endX),
                                                                       bottom=float(endY),
                                                                       label='face'),
                                          model_info={'name': self.model_entity.name,
                                                      'confidence': float(confidence)})
            batch_annotations.append(image_annotations)
        return batch_annotations
