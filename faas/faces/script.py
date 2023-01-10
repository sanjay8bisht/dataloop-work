import dtlpy as dl
import os

if dl.token_expired():
    dl.login()

package = dl.packages.get(package_name='face-detection')
print(package.id)

service = package.services.get(service_name='face-detection')

print(service.package_revision)

service.package_revision = package.version

# service.update()
project = dl.projects.get(project_name='faces-faas-triggers-3')
dataset = project.datasets.get(dataset_name='faces')
item = dataset.items.get(item_id='63b69f7b141ae1d29ab90e3b') 
print(item)
print(service.execute(project_id='9f8e66dc-328f-4edb-b934-1659d330f6bc', function_name='face_detection',
                      item_id='63b69f7b141ae1d29ab90e3b'))
