from package import Engine
from transforms import transform, transform2

engine = Engine()
first_transform = engine.transform(transform)
engine.head(first_transform)
second_transform = engine.transform(transform2)
engine.head(second_transform)