from functions import math
from rafa import *
from transforms import transform, transform_with_select

# A typical transformation
first_transform = rafa.transform(transform)

# You can run select statements here too
random_sample = rafa.select(f"select * from { first_transform } order by { math.randInt() } limit 10")
print(random_sample)

# Or even run a select inside a transformation by passing in the engine as a parameter
third_transform = rafa.transform(transform_with_select, rafa=rafa)
rafa.head(third_transform)