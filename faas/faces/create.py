import os
import dtlpy as dl

# dl.login()

if dl.token_expired():
    dl.login()

# Create Project
project_name = "faces-faas-triggers-3"
# project = dl.projects.create(project_name=project_name)
project = dl.projects.get(project_name=project_name)

# create dataset
dataset_name = "faces"
# project.datasets.create(dataset_name=dataset_name)
dataset = project.datasets.get(dataset_name=dataset_name)

gender_package_name = "gender-classification-3"
gender_function_name = "gender_classification"

face_detection_package_name = "face-detection"
face_detection_function_name = "face_detection"

filters = dl.Filters()
filters.add(field='datasetId', values=dataset.id)

# GENDER CLASSIFICATION MODULE
classification_modules = [dl.PackageModule(
    name=face_detection_package_name,
    entry_point='main.py',
    functions=[
        dl.PackageFunction(
            name=face_detection_function_name,
            inputs=[
                dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM),
            ],
            outputs=[
                dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
            ],
            description='adds gender classification to the item'
        )
    ]
)]

package = project.packages.push(package_name=face_detection_package_name,
                                modules=classification_modules,
                                src_path=os.path.join('faas', 'faces', 'functions', 'add_annotation_to_face'))
print('New Package has been deployed')

runtime = dl.KubernetesRuntime(autoscaler=dl.KubernetesRabbitmqAutoscaler(min_replicas=1,
                                                                          max_replicas=1,
                                                                          queue_length=10),
                               runner_image='docker.io/sanjay8dataloop/python-opencv:latest')

service = package.services.deploy(service_name=package.name,
                                  module_name=package.name,
                                  runtime=runtime)

# filters.add(field='dir', values='/incoming')

trigger = service.triggers.create(
    name=face_detection_package_name,
    function_name=face_detection_function_name,
    resource=dl.TriggerResource.ITEM,
    actions=dl.TriggerAction.CREATED,
    filters=filters
)
