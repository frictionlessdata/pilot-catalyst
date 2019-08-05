from collections import Counter
from datapackage import Package
from datapackage.exceptions import RelationError

# Explore data

# Get fuel
ferc1 = Package('data/ferc1-test/datapackage.json')
fuel = ferc1.get_resource('fuel_ferc1').read(keyed=True, relations=True)

# Get plants
glue = Package('data/glue-test/datapackage.json')
plants = glue.get_resource('plants').read(keyed=True)
plants_map = {row['plant_id_pudl']: row['plant_name'] for row in plants}

# Count plants
counter = {}
for row in fuel:
    plant_id_pudl = row['plant_name']['plant_id_pudl']
    plant_name = plants_map[plant_id_pudl]
    counter.setdefault(plant_name, 0)
    counter[plant_name] += 1

# Get most common plants
print('Most common plants:')
for item in Counter(counter).most_common(10):
    print('- %s: %s' % (item[0], item[1]))
