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

Table.__str__ = lambda self: f'"{self.name}"' if isinstance(self._con, sqlite3.Connection) else f'"{self.schema}"."{self.name}"'

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
                "filename": os.getenv('RAFA_SQLITE_FILENAME')
            }
            print(data)
            self.db = DB(**data)

        if debug:
            print(args)
            print(self.db.filename)
            print(self.db.tables)

        if self.db is None:
            raise Exception("DB is missing or misconfigured. Did you forget to include a config file?")

    def _get_schema(self) -> str:
        return self.config["schema"] + "." if self.config["schema"] else ""

    def _get_table_path(self, table) -> str:
        return 

    def _generate_random_name(self) -> str:
        return f"_rafa_tbl_{randrange(10000000)}"

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

    def _ctas(self, sql: str, table_name: str = None) -> str:
        """ Runs the sql block and returns a reference to the table created """
        name = self._generate_random_name() if table_name is None else table_name

        if table_name:
            self._run_ddl(f"DROP TABLE IF EXISTS \"{name}\"")

        query = f"""
            create table \"{ name }\" as
                { sql }
        """
        self._run_ddl(query)

        if not table_name:
            self.temp_tables.append(name)

        return name
    
    def select(self, sql: str):
        return self.db.query(sql)

    def close(self):
        while self.temp_tables:
            self._run_ddl(f"drop table \"{ self.temp_tables.pop() }\"")

    def transform(self, transformer, name=None, **kwargs) -> str:
        if not name:
            name = transformer.__name__.split('.')[1]
        transformed_table = self._ctas(transformer.transform(**kwargs), table_name=name)

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

        possible_tables = self.db.find_table(name)

        if schema is None:
            return possible_tables[0]

        for possibility in possible_tables:
            if possibility.schema == schema:
                return possibility

        raise Exception("cannot find source table; you may need to explicitly define a schema with source(name, schema=\"your_schema\")")

    def test(self, transformer):
        transformer.test(transformer, self)
        self.close()