import xnat
session = xnat.connect('http://xnat.ninds.nih.gov/', user='linc9', password='linc9')
experiment = session.create_object('/data/experiments/{experiment}'.format(experiment=experiment_id))

resource = experiment.resources.get('FSv6', None)

# If resource doesn't exist, just create it
if resource is None:
    resource = connection.classes.ResourceCatalog(parent=experiment, label='FSv6')

resource.upload_dir('/output/currsub')

print('done')