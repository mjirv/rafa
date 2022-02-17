def sequence(n: int):
    return f"""
        with final as (
            { " union all ".join([f"select {i} as id, 'generated row' as name" for i in range(n)]) }
        )
        select * from final
    """

def list_group_cols(groupByCols):
    return ", ".join([str(i + 1) for i in range(len(groupByCols))])