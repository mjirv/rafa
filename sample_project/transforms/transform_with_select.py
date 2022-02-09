from functions import math

def transform(rafa):
    # select returns a pandas object
    country = rafa.select(f'select * from customer order by {math.randInt()} limit 1').iloc[0].Country

    return f"select * from customer where country = '{ country }'"
