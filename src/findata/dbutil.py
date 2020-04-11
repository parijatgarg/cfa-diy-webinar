## Note: This module is not a reflection of best the best practices
#        in coding. This is a quickfix library to support the
#        demonstration of the actual code for financial analytics

'''MySQL easy-access module

This module makes access to a MySQL database very simple.
It manages the connection pools, etc, converts the returned rows into
dictionaries

For update/delete queries, it returns information about
the number of rows affected.

For insert queries, it returns the lastrowid in case the
affected table contains an auto increment column
'''

import mysql.connector
try:
    from StringIO import StringIO
except:
    from io import StringIO
    from io import BytesIO
import gzip
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import datetime



IntegrityError = mysql.connector.errors.IntegrityError

class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):
    '''This is a utility class that converts the rows returned from a MySQL
    query into a list of dictionaries where each column becomes a key'''

    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None


class Database(object):

    def __init__(self, config, pool_name='dbpool'):
        self._config = config
        self._pool_name = pool_name

    def execute_query(self, query, params=None):
        """Execute a specified query on the MySQL database.

        Args:
            query (str): The query to execute
            params (tuple): List of parameter values to match the number of
                placeholder items in the query

        Returns:
            list/dict: For select queries, returns a list of dictionaries
                       For update/delete/insert queries, returns a dictionary
                       containing *rows* (count of affected rows) and
                       *lastrowid* which contains value of any
                       auto_increment field in case of an insert
        """

        if params is not None and not isinstance(params, tuple) and not isinstance(params, dict):
            params = (params,)
        conn = mysql.connector.connect(pool_name=self._pool_name, **self._config)
        cursor = conn.cursor(cursor_class=MySQLCursorDict)
        try:
            execresult = cursor.execute(query, params)
        except Exception as e:
            conn.close()
            raise e
        try:
            # if an insert or update query was called, an exception will result.
            # in that case, we return the count of inserted/updated rows
            # and the lastrowid in case there is an auto-increment field
            results = cursor.fetchall()
            conn.commit()
        except:
            conn.commit()
            results = {'rows':cursor.rowcount, 'lastrowid':cursor.lastrowid}
        conn.close()
        return results



def compress(self, data):
    try:
        compressed = BytesIO()
    except:
        compressed = StringIO()
    f = gzip.GzipFile('', 'wb', 9, compressed)
    f.write(data)
    f.close()
    value = compressed.getvalue()
    compressed.close()
    return value


def decompress(self, data):
    try:
        data = StringIO(data)
    except:
        data = BytesIO(data)
    f = gzip.GzipFile('', 'rb', 9, data)
    output = f.read()
    f.close()
    return output