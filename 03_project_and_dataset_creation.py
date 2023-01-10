import datetime
import dtlpy as dl
# dl.login()

if dl.token_expired():
    dl.login()

# Create Project
# project = dl.projects.create(project_name='My-First-Project')
project = dl.projects.get(project_name='My-First-Project')

# # Create Dataset
# project.datasets.create(dataset_name='My-First-Dataset')

# # Upload items
dataset = project.datasets.get(dataset_name='My-First-Dataset')
# dataset.items.upload(local_path='/Users/meena392/Downloads/flowers/daisy/5547758_eea9edfd54_n.jpg')
# dataset.items.upload(local_path='/Users/meena392/Downloads/flowers/daisy/5673728_71b8cb57eb.jpg')

# # Get Item
# item = dataset.items.get(item_id='63b3046841f3b36b807abd2e')    # Image 1
item = dataset.items.get(item_id='63b30468347ba82283f4a629')    # Image 2
# item.print()

# # Get all items
# pages = dataset.items.list()
# for item in pages.all():
#     item.print()

# Annotating Items
## Classification ##
"""
The SDK can add Classification labels to an Item using 2 steps.

    1) Adding a label to a dataset’s Recipe.
    2) Adding the label to an item as a Classification.
"""
# This will add label to default recipe, default recipe is created whenever you create a dataset
# 1) Run the following command to add a Label (Person) to the My-First-Dataset dataset recipe.
dataset.add_label(label_name='Flower')

# # 2) Run the following commands to Annotate and Upload the label (Daisy) as a Classification to the item (item)
builder = item.annotations.builder()
builder.add(annotation_definition=dl.Classification(label='Flower'))
item.annotations.upload(builder)

## Point Markers ##
dataset.add_label(label_name='Lilly')
builder.add(annotation_definition=dl.Point(x=0, y=30, label='Lilly'))
builder.add(annotation_definition=dl.Point(x=270, y=30, label='Lilly'))
builder.add(annotation_definition=dl.Point(x=0, y=232, label='Lilly'))
builder.add(annotation_definition=dl.Point(x=270, y=232, label='Lilly'))
item.annotations.upload(builder)

# Working with Filters
## Creating Filters
# my_filter = dl.Filters()
# my_filter.add_join(field='type', values='point')
# my_filter.add_join(field='label', values='Lilly')

# pages = dataset.items.list(filters=my_filter)
# for item in pages.all():
#     item.print()


# Using Filters to Replace Data
# flower_filter = dl.Filters(resource=dl.FILTERS_RESOURCE_ITEM)
# flower_filter.add_join(field='label', values='Flower')

# pages = dataset.items.list(filters=flower_filter)
# for item in pages.all():
#     item.print()

# dataset.add_label(label_name='Flowers')
# person_ann_filter = dl.Filters(resource=dl.FiltersResource.ANNOTATION)
# person_ann_filter.add(field='label', values='Flower')
# pages = dataset.items.list(filters=person_ann_filter)

# for item in pages.all():
#     item.print()
#     annotations = item.annotations.builder()
#     annotations.add(annotation_definition=dl.Classification(label='Flowers'))
#     item.annotations.upload(annotations)
#     item.annotations.delete(filters=person_ann_filter)

# # Adding a New User Metadata Field to an Item
print(item.metadata)

now = datetime.datetime.now().isoformat()
# modify metadata for the item
item.metadata['user'] = dict()
# add it to the item's metadata
item.metadata['user']['dateTime'] = now
# update the item
item = item.update()


# Creating Tasks
filters = dl.Filters()
filters.add_join(field='label', values='Flower')

pages = dataset.items.list(filters=filters)
for item in pages.all():
    item.print()

task = dataset.tasks.create(task_name='test',
                            due_date=datetime.datetime(day=2, month=1, year=2023).timestamp(),
                            assignee_ids=['JohnDoe@gmail.com', 'JohnDoe2@gmail.com'],
                            filters=filters)