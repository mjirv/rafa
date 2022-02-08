from functions import math
from package import Engine

def transform(engine: Engine):
    country = engine.select(f'select * from customer order by {math.randInt()} limit 1').iloc[0].Country
    return f"select * from customer where country = '{ country }'"
