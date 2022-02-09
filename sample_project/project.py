from functions import math
from jules import *
from transforms import transform, transform_with_select

# A typical transformation
first_transform = jules.transform(transform)

# You can run select statements here too
random_sample = jules.select(f"select * from { first_transform } order by { math.randInt() } limit 10")
print(random_sample)

# Or even run a select inside a transformation by passing in the engine as a parameter
third_transform = jules.transform(transform_with_select, jules=jules)
jules.head(third_transform)