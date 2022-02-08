from package import Engine
from transforms import transform, transformer

engine = Engine()
first_transform = engine.transform(transform)
engine.head(first_transform)
second_transform = engine.transform(second_transform)
engine.head(second_transform)