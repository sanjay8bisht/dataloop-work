# Artifacts
> Artifacts are nothing but large supporting files needed to run any code. Like xml, pb or caffemodel file needed to run any ML model.

Since we need to minimise the code size, we need to upload these large files as artifacts to the cloud.

Inorder to upload artifacts we need to deploy the package first.

Below is a code snippet to upload n number of artifacts to a package.

```python
import dtlpy as dl

package_name = 'your-package-name'
artifacts = ['/path/to/xml/file/file.xml', '/path/to/pb/file/file.pb',
             '/path/to/caffemodel/file/file.caffemodel']

package = dl.packages.get(package_name=package_name)

for artifact in artifacts:
    package.artifacts.upload(filepath=artifact,
                            package=package,
                            package_name=package.name)
```

> List & Download artifacts

```python
package = dl.packages.get(package_name='gender-classification-3')
print(package.id)
print('artifacts', package.artifacts.list().print())

faceProto = "opencv_face_detector.pbtxt"
full_faceProto_path = os.path.join(os.getcwd(), 'artifacts', faceProto)
print(full_faceProto_path)
package.artifacts.download(artifact_name=faceProto, 
                           local_path=full_faceProto_path)
```