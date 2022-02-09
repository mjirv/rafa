from db import DemoDB
from random import randrange

class _Engine:
    def __init__(self) -> "_Engine":
        """Takes in some yaml (json?) files and sets up the connection"""
        self.db = DemoDB()
        self.temp_tables = []

    def config(self):
        return

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

    def _ctas(self, sql: str, table_name: str = None) -> str:
        """ Runs the sql block and returns a reference to the table created """
        name = self._generate_random_name() if table_name is None else table_name
        print(name) 

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

    def transform(self, transformer, **kwargs) -> str:
        transformed_table = self._ctas(transformer.transform(**kwargs), table_name=transformer.__name__.split('.')[1])
        
        # remove any temp tables created by the transformer
        self.close()

        return transformed_table

rafa = _Engine()