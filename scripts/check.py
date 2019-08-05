from datapackage import Package
from datapackage.exceptions import RelationError

# Check relations

package = Package('data/ferc1-test/datapackage.json')
try:
    package.get_resource('fuel_ferc1').check_relations()
    print('Relations are checked')
except RelationError as exception:
    print(exception)
