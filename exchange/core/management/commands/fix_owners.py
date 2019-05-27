from geonode.people.models import Profile
from geonode.documents.models import Document
from geonode.maps.models import Map
from geonode.layers.models import Layer

try:
    admin_user = Profile.objects.get(username='admin')
except Profile.DoesNotExist:
    # Somehow we couldn't find the admin user, so fail the script
    print('Failed to find admin user for Exchange - exiting script')

bad_data = []

for document in Document.objects.all():
    if document.owner is None:
        document.owner = admin_user
        document.save()
        bad_data.append({
            'title': document.title,
            'type': 'Document'
        })
for layer in Layer.objects.all():
    if layer.owner is None:
        layer.owner = admin_user
        layer.save()
        bad_data.append({
            'title': layer.title,
            'type': 'Layer'
        })
for map_obj in Map.objects.all():
    if map_obj.owner is None:
        map_obj.owner = admin_user
        map_obj.save()
        bad_data.append({
            'title': map_obj.title,
            'type': 'Map'
        })

print('Corrected {0} data objects which lacked an owner'.format(len(bad_data)))
for item in bad_data:
    print('{0} {1} assigned to admin user'.format(item['type'], item['title']))
print('Contact your Exchange administrator to assign them the correct owner')
