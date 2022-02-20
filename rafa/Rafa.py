import json
import os
from db import DB, DemoDB
from dotenv import load_dotenv
from random import randrange

class Rafa:
    def __init__(self, demo=False, config_path='config.yml', debug=False) -> "Rafa":
        """Takes in some configuration variables and sets up the connection"""
        self.temp_tables = []
        self.db = None

        ### Initialize database ###
        data = {}
        if demo:
            self.db = DemoDB()
        
        else:
            if config_path:
                with open(config_path, 'r') as f:
                    data = json.load(f)
            else:
                # Load from env file
                load_dotenv()
                data = {
                    "hostname": os.getenv('RAFA_HOSTNAME'),
                    "username": os.getenv('RAFA_USERNAME'),
                    "password": os.getenv('RAFA_PASSWORD'),
                    "port": os.getenv('RAFA_PORT'),
                    "dbname": os.getenv('RAFA_DBNAME'),
                    "dbtype": os.getenv('RAFA_DBTYPE'),
                    "filename": os.getenv('RAFA_SQLITE_FILENAME')
                }
            self.db = DB(**data)

        if debug:
            print(self.db.filename)
            print(self.db.tables)

        if self.db is None:
            raise Exception("DB is missing or misconfigured. Did you forget to include a config file?")

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

    def source(self, name: str):
        return name

    def test(self, transformer):
        transformer.test(transformer, self)
        self.close()