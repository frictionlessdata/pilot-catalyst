from datapackage import Package
from datapackage.exceptions import RelationError

# Dereference relations

package = Package('data/ferc1-test/datapackage.json')
try:
    keyed_rows = package.get_resource('fuel_ferc1').read(keyed=True, relations=True)
    print(keyed_rows[0])
except RelationError as exception:
    print(exception)
