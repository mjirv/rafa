from functions import utils

def transform(engine):
    tmp = engine.do(utils.sequence(10))
    engine.head(tmp)
