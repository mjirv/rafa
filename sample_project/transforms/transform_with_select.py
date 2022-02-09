from functions import math

def transform(jules):
    # select returns a pandas object
    print(jules.name)
    country = jules.select(f'select * from customer order by {math.randInt()} limit 1').iloc[0].Country

    return f"select * from customer where country = '{ country }'"
