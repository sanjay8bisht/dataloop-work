import os

import dtlpy as dl
from adapter import SimpleModelAdapter

project_name = "mm-face-detection"
dataset_name = "faces"
face_detection_package_name = "face-detection-model"
weight_filename = 'res10_300x300_ssd_iter_140000.caffemodel'

project = dl.projects.get(project_name=project_name)
dataset = project.datasets.get(dataset_name=dataset_name)
codebase = project.codebases.pack(directory='./',
                                  name="face-detection")
metadata = dl.Package.get_ml_metadata(cls=SimpleModelAdapter,
                                      default_configuration={'input_size': 256},
                                      output_type=dl.AnnotationType.BOX
                                      )
module = dl.PackageModule.from_entry_point(entry_point='adapter.py')

package = project.packages.push(package_name=face_detection_package_name,
                                # src_path=os.getcwd(),
                                package_type='ml',
                                codebase=codebase,
                                modules=[module],
                                is_global=False,
                                service_config={
                                    'runtime': dl.KubernetesRuntime(pod_type=dl.INSTANCE_CATALOG_GPU_K80_S,
                                                                    autoscaler=dl.KubernetesRabbitmqAutoscaler(
                                                                        min_replicas=0,
                                                                        max_replicas=1),
                                                                    concurrency=1).to_json()},
                                metadata=metadata)

# artifact = dl.LocalArtifact(local_path='<path to weights>')
model_weight_url = 'https://github.com/vinuvish/Face-detection-with-OpenCV-and-deep-learning/blob/master/models/res10_300x300_ssd_iter_140000.caffemodel'
# model_proto_url = 'https://github.com/vinuvish/Face-detection-with-OpenCV-and-deep-learning/blob/master/models/res10_300x300_ssd_iter_140000.caffemodel'
artifacts = dl.LinkArtifact(url=model_weight_url, filename=weight_filename)
model = package.models.create(model_name='face-detection-opencv',
                              description='face detection model in opencv',
                              tags=['pretrained', 'tutorial'],
                              dataset_id=None,
                              project_id=package.project.id,
                              model_artifacts=[artifacts],
                              status='trained'
                              )

model.deploy()

# adapter = package.build()
# adapter.load_from_model(model_entity=model)
#
# pred = adapter.predict_items(dl.items.get(id=''))
#
# print(pred)