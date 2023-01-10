# Package
>Package can be thought of like a docker image, which will have our all our code.
> 
> package = Docker image
```python
package_name = '<package_name>'
module_name = '<module_name>'
package = project.packages.push(package_name=package_name,
                                modules=module_name,
                                src_path=os.path.join('folder', 'to', 'package'))
```

# Service
>Service can be thought of like container of an image(here package)
> 
> service = Docker container
> 
> The above package will be deployed as a service with appropriate runtime
```python
runtime = dl.KubernetesRuntime(autoscaler=dl.KubernetesRabbitmqAutoscaler(min_replicas=1,
                                                                          max_replicas=1,
                                                                          queue_length=10))

service = package.services.deploy(service_name=package.name,
                                  module_name=package.name,
                                  runtime=runtime)
```