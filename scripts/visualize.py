from elasticsearch import Elasticsearch
from datapackage import Package
from tableschema_elasticsearch import Storage

# Get resource
package = Package('data/ferc1-test/datapackage.json')
resource = package.get_resource('fuel_ferc1')

# Create storage
engine=Elasticsearch()
storage=Storage(engine)

# Write data
storage.create('ferc1-test', [('fuel_ferc1', resource.schema.descriptor)])
list(storage.write('ferc1-test', 'fuel_ferc1', resource.read(keyed=True), ['id']))
