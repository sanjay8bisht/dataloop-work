import dtlpy as dl


class ServiceRunner(dl.BaseServiceRunner):
    def run(self, item):
        filters = dl.Filters(resource=dl.FiltersResource.ANNOTATION)
        filters.add(field='type', values='box')
        if len(item.annotations.list(filters=filters)) > 0:
            return item