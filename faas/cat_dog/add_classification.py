import dtlpy as dl

if dl.token_expired():
    dl.login()


project_name = "cat-dog-faas-triggers"
dataset_name = "cat-dogs"
package_name = "add-classification"

project = dl.projects.get(project_name=project_name)
dataset = project.datasets.get(dataset_name=dataset_name)

modules = [dl.PackageModule(
    name=package_name,
    entry_point='main.py',
    functions=[
        dl.PackageFunction(
            name='add_classification',
            inputs=[
                dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM),
            ],
            outputs=[
                dl.FunctionIO(name='items', type=dl.PackageInputType.ITEMS)
            ],
            description='adds a classification to the item'
        )
    ]
)]

package = project.packages.push(package_name=package_name,
                                modules=modules,
                                src_path='./functions/add_annotation_to_item')
print('New Package has been deployed')

runtime = dl.KubernetesRuntime(autoscaler=dl.KubernetesRabbitmqAutoscaler(min_replicas=0,
                                                                          max_replicas=1,
                                                                          queue_length=10))

service = package.services.deploy(service_name=package.name,
                                  module_name=package.name,
                                  runtime=runtime)

filters = dl.Filters()
filters.add(field='datasetId', values=dataset.id)
# filters.add(field='dir', values='/incoming')

trigger = service.triggers.create(
    name='add-classification',
    function_name='add_classification',
    resource=dl.TriggerResource.ITEM,
    actions=[dl.TriggerAction.CREATED],
    filters=filters
)
