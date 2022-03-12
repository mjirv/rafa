import argparse
import os
import sqlite3
from db import db, DemoDB
from dotenv import load_dotenv
from random import randrange

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')
argRun = subparser.add_parser('run')
argInit = subparser.add_parser('init')

argRun.add_argument('--profile', help="the profile to use, e.g. \"--profile staging\" uses `profiles/.env.staging`")
argInit.add_argument('name', help="the name of the project to create")
args = parser.parse_args()

# Override db.py's Table class str representation for easier querying
DB = db.DB
Table = db.Table

class Rafa:
    def __init__(self, demo=False, config_path='profiles/.env.default', debug=False) -> "Rafa":
        """Takes in some configuration variables and sets up the connection"""
        self.temp_tables = []
        self.db = None

        if args.profile:
            config_path=f'profiles/.env.{args.profile}'
        load_dotenv(config_path)

        self.config = {
            "source_schema": '"' + os.getenv('RAFA_SOURCE_SCHEMA') + '"' if os.getenv('RAFA_SOURCE_SCHEMA') else None,
            "schema": '"' + os.getenv('RAFA_SCHEMA') + '"' if os.getenv('RAFA_SCHEMA') else None
        }

        ### Initialize database ###
        data = {}
        if demo:
            self.db = DemoDB()
        elif config_path:
            data = {
                "hostname": os.getenv('RAFA_HOSTNAME'),
                "username": os.getenv('RAFA_USERNAME'),
                "password": os.getenv('RAFA_PASSWORD'),
                "port": os.getenv('RAFA_PORT'),
                "dbname": os.getenv('RAFA_DBNAME'),
                "dbtype": os.getenv('RAFA_DBTYPE'),
                "filename": os.getenv('RAFA_SQLITE_FILENAME'),
                "bq_project": os.getenv('BIGQUERY_PROJECT'),
                "bq_default_dataset": os.getenv('BIGQUERY_DEFAULT_DATASET')
            }
            self.db = DB(**data)

        if debug:
            print(args)
            print(self.db.filename)
            print(self.db.tables)

        if self.db is None:
            raise Exception("DB is missing or misconfigured. Did you forget to include a config file?")

        self._is_sqlite = isinstance(self.db.con, sqlite3.Connection)
        self._is_bigquery = self.db.dbtype == 'bigquery'

        if self._is_sqlite:
            Table.__str__ = lambda self: f'"{self.name}"'
        elif self._is_bigquery:
            Table.__str__ = lambda self: f'{self.schema}.{self.name}'
        else:
            Table.__str__ = lambda self: f'"{self.schema}"."{self.name}"'

    def _get_schema(self) -> str:
        return self.config["schema"] + "." if self.config["schema"] else ""

    def _get_table_path(self, schema: str, name: str) -> str:
        if schema is None or self._is_sqlite:
            return f'{name}'
        else:
            return f'{schema}.{name}'

    def _get_table(self, name, schema=None, allow_none=False) -> str:
        # Refresh schema so that we get the latest tables
        if self._is_sqlite:
            self.db._create_sqlite_metatable()

        self.db.refresh_schema()

        possible_tables = self.db.find_table(name)

        if len(possible_tables) == 1:
            return possible_tables[0]

        if schema is None:
            schema = self.config["schema"]

        for possibility in possible_tables:
            if possibility.schema == schema:
                return possibility

        if not allow_none:
            raise Exception(f"cannot find table \"{name}\"; you may need to explicitly define a schema with source(name, schema=\"your_schema\")")

        return None

    def _generate_random_name(self) -> str:
        return f"rafa_tbl_{randrange(10000000)}"

    def _run_ddl(self, query):
        try:
            self.db.query(query)
        except TypeError as typeError:
            if (str(typeError) == '\'NoneType\' object is not iterable'):
                # DDL statement succeeded
                return
            raise typeError

    def head(self, table: str):
        """ Runs a SQL block against the connection"""
        print(self.db.query(f"select * from {table}").head())

    def select_all(self, table: str):
        return self.db.query(f"select * from {table}")

    def _ctas(self, sql: str, table_name: str = None, schema: str = None) -> str:
        """ Runs the sql block and returns a reference to the table created """
        name = self._generate_random_name() if table_name is None else table_name

        table = self._get_table(name, schema, allow_none=True)

        # if the randomly-generated name conflicts (unlikely), try again with a new name
        while table and not table_name:
            name = self._generate_random_name()
            table = self._get_table(name, schema, allow_none=True)

        if table_name:
            self._run_ddl(f"DROP TABLE IF EXISTS {table}")

        table_path = str(table) if table is not None else self._get_table_path(schema, name)

        query = f"""
            create table {table_path} as
                { sql }
        """
        self._run_ddl(query)
        table = self._get_table(name, schema)

        if not table_name:
            self.temp_tables.append(table)

        return table
    
    def select(self, sql: str):
        return self.db.query(sql)

    def close(self):
        while self.temp_tables:
            self._run_ddl(f"drop table { self.temp_tables.pop() }")

    def transform(self, transformer, name=None, schema=None, **kwargs) -> str:
        if not name:
            name = transformer.__name__.split('.')[1]
        transformed_table = self._ctas(transformer.transform(**kwargs), table_name=name, schema=schema)

        print(f"- transformed {name}")
        
        # remove any temp tables created by the transformer
        self.close()

        return transformed_table

    def temp_transform(self, transformer, **kwargs) -> str:
        return self._ctas(transformer.transform(**kwargs))

    def temp_from_records(self, records) -> str:
        sql = " union all ".join(["select" + ", ".join([f"""
            {value} as {key}
        """ for key, value in record.items()]) for record in records])
        return self._ctas(sql)

    def source(self, name: str, schema: str = None) -> Table:
        if schema is None:
            schema = self.config["source_schema"]

        return self._get_table(name, schema)

    def test(self, transformer):
        transformer.test(transformer, self)
        self.close()