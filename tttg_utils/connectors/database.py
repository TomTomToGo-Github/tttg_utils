## built-in modules
import os
import sqlite3
from contextlib import contextmanager
## pip installed modules
import psycopg2
import pandas as pd


class QueryDB:

    def __init__(self, db_connection=None):
        if not db_connection:
            self.db_connection = None
            self.license_db = sqlite3
        else:
            db_connection = db_connection
            self.license_db = psycopg2

    @contextmanager
    def open_db(self, db_name):
        try:
            if not self.db_connection:
                conn = self.license_db.connect(db_name)
            else:
                conn = self.license_db.connect(
                    database=self.db_connection['db_name'],  # must exist -> or break code
                    user=self.db_connection.get('db_user', 'postgres'),  # default postgres
                    password=self.db_connection.get('db_pw', ''),  # default empty
                    host=self.db_connection.get('db_host', 'localhost'),  # default localhost
                    port=self.db_connection.get('db_host', '5432')  # default 5432
                )
            cursor = conn.cursor()
            yield cursor
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            # Commit changes to the database and close the cursor and connection when done
            conn.commit()
            cursor.close()
            conn.close()

    def update_db(self, db_name, executions):
        with self.open_db(db_name) as cursor:
            for exec in executions:
                if isinstance(exec, tuple):
                    command = exec[0]
                    values = exec[1]
                    cursor.execute(command, values)
                else:
                    cursor.execute(exec)

    def fetch_from_db(self, db_name, table_name, fieldname, fieldvalue):
        with self.open_db(db_name) as cursor:
            # Retrieve data from the table
            cursor.execute(f"SELECT * FROM {table_name} WHERE {fieldname} == '{fieldvalue}'")
            entries_for_user = list(cursor.fetchall())

        return entries_for_user



# Objects of this class can store Database information and fetch the data of loaded queries
class PGSQL_Query_Class():
    def __init__(self):
        self.host = os.getenv("DBHOST")
        self.dbname = os.getenv("DBDATABASE")
        self.user = os.getenv("DBUSER")
        self.password = os.getenv("DBTOKEN")
        if self.host is None:
            m1 = "\n\nNo DB found in .env when initializing the 'PSQL_Query_Class'-instance. "
            m2 = "Host, database name, username and password must be loaded separately."
            print(m1, m2)

    def load_SQLQueryFile(self, query_path):
        fd = open(query_path)
        self.sql_query = fd.read()
        fd.close()

    def fetchData(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # connect to the PostreSQL server
            print('            - Connecting to the PostgreSQL database...')
            if self.host == 0:
                print('You have not loaded the "host" database information to to query object!')
            conn = psycopg2.connect(
                host=self.host,
                database=self.dbname,
                user=self.user,
                password=self.password
            )
            # create a cursor
            cur = conn.cursor()
            # execute a statement
            print('            - Executing query...')
            cur.execute(self.sql_query)
            # save data in a dataframe
            colnames = [desc[0] for desc in cur.description]
            df = pd.DataFrame(cur.fetchall(), columns=colnames)
            print('            - Data fetched.')
            # close the communication with the PostgreSQL
            cur.close()
            return df
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('            - Database connection closed.')

    def create_role(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # connect to the PostreSQL server
            print('            - Connecting to the PostgreSQL databse...')
            if self.host == 0:
                print('You have not loaded the "host" database information to to query object!')
            conn = psycopg2.connect(host=self.host,
                                    database=self.dbname,
                                    user=self.user,
                                    password=self.password
                                    )
            # create a cursor
            cur = conn.cursor()
            # execute a statement
            print('            - Executing query: ', self.sql_query)
            cur.execute(self.sql_query)
            # close the communication with the PostgreSQL
            cur.close()
            # commit the changes - apply executes to DB
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('            - Database connection closed.')