from functions.utils import list_group_cols

def transform(period=None, sources=[], groupByCols=[], join=None):
    date_periods = {
        'day': '%Y-%m-%d',
        'week': '%Y-%W',
        'month': '%Y-%m',
        'year': '%Y'
    }

    return f"""
        select 
            { f"strftime('{ date_periods[period] }', InvoiceDate) as {period}," if period else "" }
            { ", ".join(groupByCols) + "," if groupByCols != [] else "" }
            sum(Total) as revenue
        from { sources['invoices'] } invoices
        { f"left join { sources[join['name']] } {join['name']} using ({ join['on'] })" if join else "" }

        group by { list_group_cols(groupByCols + ([period] if period is not None else []))}
        order by 1, 2
    """