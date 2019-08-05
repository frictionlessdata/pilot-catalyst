# Pilot Catalyst

This is a short introduction to the FrictionlessData software for the PUDL by Catalyst project.

> Code and data for this article is available here https://github.com/frictionlessdata/pilot-catalyst

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

## Checking relations

### datapackage

Let's check the `ferc1-test.fuel_ferc1`'s relations. Because the data in the repository is valid we will get sucesseful results:

```python
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
