import dtlpy as dl
import os

if dl.token_expired():
    dl.login()

package = dl.packages.get(package_name='gender-classification-3')
print(package.id)
print('artifacts', package.artifacts.list().print())

faceProto = "opencv_face_detector.pbtxt"
full_faceProto_path = os.path.join(os.getcwd(), 'artifacts', faceProto)
print(full_faceProto_path)
package.artifacts.download(artifact_name=faceProto,
                           local_path=full_faceProto_path)
