# Pilot Catalyst

This is a short introduction to the FrictionlessData software for the PUDL by Catalyst project.

> Code and data for this article is available [here](https://github.com/frictionlessdata/pilot-catalyst). After cloning the repo run `pip install -r requirements.txt` to install dependencies. All code beclow can be run using `python script/<name>.py`

## Datasets

We use two data packages:
- `ferc1-test`
- `glue-test`

The idea behind the `glue-test` data package is to have a reference table for other data packages. For example, the `ferc1-test.fuel_ferc1` resource has a foreign keys definition:

> Here is used an experimental support of external foreign keys implemented at https://github.com/frictionlessdata/datapackage-py/tree/fk-external

```json
"foreignKeys": [
    {
        "fields": "utility_id_ferc1",
        "reference": {
            "package": "../glue-test/datapackage.json",
            "resource": "plants_ferc",
            "fields": "utility_id_ferc1"
        }
    },
    {
        "fields": "plant_name",
        "reference": {
            "package": "../glue-test/datapackage.json",
            "resource": "plants_ferc",
            "fields": "plant_name"
        }
    }
],
```

## Checking Relations

### datapackage

Let's check the `ferc1-test.fuel_ferc1`'s relations. Because the data in the repository is valid we will get sucesseful results:

```python
from datapackage import Package
from datapackage.exceptions import RelationError

# Check relations

package = Package('data/ferc1-test/datapackage.json')
try:
    package.get_resource('fuel_ferc1').check_relations()
    print('Relations are checked')
except RelationError as exception:
    print(exception)

# Output
# ------
# Relations are checked
```

Now, we will remove some data from the reference table `glue-test.plants_ferc`:

```bash
sed -i '2d' data/glue-test/data/plants_ferc.csv
# deleting the "164,*dolet hills (3),1" row
```

And run the Python script again:

```python
# Output
# ------
# Foreign key "['plant_name']" violation in row "326"
```

Looking at row 326 of the `ferc1-test.fuel_ferc1` resource we see the now data is not valid because the foreign key constraint is not satisfied for the field `plant_name` with the value `*dolet hills (3)`:

```csv
324,f1_fuel_2017_164_1_10,164,2017,*dolet hills (3),coal,ton,659596.0,13.868,51.87,76.77,3.74
```

### goodtables

> The Foreing Keys check is not a part of `goodtables` because it's not a part of the [`Data Quality Spec`](https://github.com/frictionlessdata/data-quality-spec/blob/master/spec.json). As a part of this pilot we can implement an [advanced check](https://github.com/frictionlessdata/data-quality-spec/blob/master/spec.json) to validate foreign keys including external foreign keys support.

## Dereferencing Relations

Let's read the `ferc1-test.fuel_ferc1` resource dereferencing relations. In this case, every row will have data from both data packages:
- `ferc1-test` (provides data for top-level fields)
- `glue-test` (provides data for `utility_id_ferc1` and `plant_name`)

```python
from datapackage import Package
from datapackage.exceptions import RelationError

# Dereference relations

package = Package('data/ferc1-test/datapackage.json')
try:
    keyed_rows = package.get_resource('fuel_ferc1').read(keyed=True, relations=True)
    print(keyed_rows[0])
except RelationError as exception:
    print(exception)

# Output
# ------
# {
#   'id': 0,
#   'record_id': 'f1_fuel_2017_122_0_4',
#   'utility_id_ferc1': {
#     'utility_id_ferc1': 122,
#     'plant_name': 'aberdeen #1',
#     'plant_id_pudl': 9
#   },
#   'report_year': 2017,
#   'plant_name': {
#     'utility_id_ferc1': 95,
#     'plant_name': 'coyote',
#     'plant_id_pudl': 132
#   },
#   'fuel_type_code_pudl': 'coal',
#   'fuel_unit': 'ton',
#   'fuel_qty_burned': Decimal('225315.0'),
#   'fuel_mmbtu_per_unit': Decimal('13.925999999999998'),
#   'fuel_cost_per_unit_burned': Decimal('26.842'),
#   'fuel_cost_per_unit_delivered': Decimal('26.842'),
#   'fuel_cost_per_mmbtu': Decimal('1.928')}
```

## Exploring Data

Let's use the data we have to get some computed information. **It shows how one can use FD software to explore PUDL data.** Here we look at `fuel-test.plants` to get normilized plant names and use foreign keys dereferencing to get most common plant names:

```python
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

# Output
# ------
# Most common plants:
#  - Weston: 10
#  - Iatan: 9
#  - Rockport: 8
#  - Mitchell (WV): 8
#  - La Cygne: 8
#  - w: 7
#  - Columbia (WI): 7
#  - Pulliam: 7
#  - Edgewater: 6
#  - Yucca: 6
```

## Exporting Data (SQL)

Let's now export the `glue-test` data package to a relational database (PostgreSQL). It's the most popular driver for `tableschema/datapackage` but the same can be done for `bigquery`, `pandas` and other "storages":

```python
from sqlalchemy import create_engine
from datapackage import Package

DATABASE_URL = 'postgresql://roll:roll@localhost:5432/pudl'

# Export data

package = Package('data/glue-test/datapackage.json')
package.save(storage='sql', engine=create_engine(DATABASE_URL))
```

We will checks the exported data using PgAdmin3. **Using FD software one can export PUDL data to SQL and then explore it as a normal relational database**. As we can see the foreign key constaints are exported as well:

![](https://i.imgur.com/l8ysDKV.png)

> There is no support for external foreign keys for SQL export at the moment.

## Visualising Data (ElasticSearch)

> To be written

## Getting Data (Datapackage Pipelines)

> To be written
