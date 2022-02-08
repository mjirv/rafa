from functions import math
from package import Engine
from transforms import transform, transform_with_select

engine = Engine()

# A typical transformation
first_transform = engine.transform(transform)

# You can run select statements here too
random_sample = engine.select(f"select * from { first_transform } order by { math.randInt() } limit 10")
print(random_sample)

# Or even run a select inside a transformation by passing in the engine as a parameter
third_transform = engine.transform(transform_with_select, engine=engine)
engine.head(third_transform)