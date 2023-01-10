import os
import dtlpy as dl

project_name = "faces-faas-triggers"
package_name = 'artifacts-package'
artifacts = ['opencv_face_detector.pbtxt', 'opencv_face_detector_uint8.pb',
             'gender_deploy.prototxt', 'gender_net.caffemodel', 'haarcascade_frontalface_default.xml']

package = dl.packages.get(package_name='gender-classification-3')

for artifact in artifacts:
    package.artifacts.upload(filepath=artifact,
                             package=package,
                             package_name=package.name)
