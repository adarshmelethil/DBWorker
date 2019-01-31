

from .msaccess import MSAccess
from .sqlite import SQLite
from .query import Query

DB_TYPES = {
	"MSAccess": MSAccess, 
	"SQLite": SQLite
}

def getDatabase(db_type, location, *args, **kwargs):
	return DB_TYPES[db_type](location, *args, **kwargs)
