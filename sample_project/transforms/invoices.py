def transform(sources):
    return f"""
        with invoice_totals as (
            select 
                "InvoiceId"
                , sum("Quantity" * "UnitPrice") as total_price
            from {sources['invoice_items']}
            group by 1
        )

        select invoices.*, total_price
        from {sources['invoices']} invoices
        left join invoice_totals
        using ("InvoiceId")
    """