from sqlalchemy import create_engine
from datapackage import Package

DATABASE_URL = 'postgresql://roll:roll@localhost:5432/pudl'

# Export data

package = Package('data/glue-test/datapackage.json')
package.save(storage='sql', engine=create_engine(DATABASE_URL))
