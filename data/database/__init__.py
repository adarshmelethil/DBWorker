
try:
	from data.database.msaccess import MSAccess
	from data.database.sqlite import SQLite
except ImportError:
	from database.msaccess import MSAccess
	from database.sqlite import SQLite

DB_TYPES = {
	"MSAccess": MSAccess, 
	"SQLite": SQLite
}

def getDatabase(db_type, location, *args, **kwargs):
	return DB_TYPES[db_type](location, *args, **kwargs)
