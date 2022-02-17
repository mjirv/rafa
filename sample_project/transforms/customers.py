def transform(sources):
    return f"""
        select * from {sources['customers']}
    """