from db import DemoDB
from random import randrange

class Engine:
    def __init__(self) -> "Engine":
        """Takes in some yaml (json?) files and sets up the connection"""
        self.db = DemoDB()
        self.temp_tables = []

    def _generate_random_name(self) -> str:
        return f"tbl_{randrange(1000000)}"

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

    def ctas(self, sql: str, table_name: str = None) -> str:
        """ Runs the sql block and returns a reference to the table created """
        name = self._generate_random_name() if table_name is None else table_name 

        if table_name:
            self._run_ddl(f"DROP TABLE {name}")

        query = f"""
            create table { name } as
                { sql }
        """
        self._run_ddl(query)

        if not table_name:
            self.temp_tables.append(name)

        return name

    def do(self, sql, how='ctas'):
        """ Runs a command """
        methods = {
            'ctas': self.ctas,
        }

        return methods[how](sql)

    def close(self):
        for table in self.temp_tables:
            self._run_ddl(f"drop table { table }")

    def transform(self, transformer, **kwargs) -> str:
        return self.ctas(transformer.transform(**kwargs), table_name=transformer.__name__.split('.')[1])
