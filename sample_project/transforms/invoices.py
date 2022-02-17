def transform(sources):
    return f"""
        with invoice_totals as (
            select 
                "InvoiceId"
                , sum("Quantity") as Quantity
            from {sources['invoice_items']}
            group by 1
        )

        select 
            invoices.*
            , Quantity
        from {sources['invoices']} invoices
        left join invoice_totals
            on invoices.InvoiceId = invoice_totals.InvoiceId
    """