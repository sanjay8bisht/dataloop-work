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
Each package will depend on modules. A module can be think of like collection code, where we define module name, code's entry point file and functions list.

```python
import dtlpy as dl

modules = [dl.PackageModule(
    name='<module_name>',
    entry_point='main.py',
    functions=[
        dl.PackageFunction(
            name='<function_name_inside_main.py>',
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
```

## Inputs/Outputs
1. Inputs - Arguments for function
2. Outputs - Values function returns