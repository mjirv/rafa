from functions.utils import list_group_cols
from functions.dates import date_trunc

def transform(period=None, sources=[], groupByCols=[], join=None):
    groupNumbers = list_group_cols(groupByCols + ([period] if period is not None else []))

    return f"""
        select 
            { f"{date_trunc(period, 'InvoiceDate')} as {period}," if period else "" }
            { ", ".join(groupByCols) + "," if groupByCols != [] else "" }
            sum(Total) as revenue
        from { sources['invoices'] } invoices
        { f"left join { sources[join['name']] } {join['name']} using ({ join['on'] })" if join else "" }

        group by { groupNumbers }
        order by { groupNumbers }
    """