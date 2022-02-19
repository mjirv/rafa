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

def test(self, rafa):
    mock_src_invoices = rafa.temp_from_records([{
        "InvoiceId": 1
    }])

    mock_src_invoice_items = rafa.temp_from_records([
        {
            "InvoiceItemId": 1,
            "InvoiceId": 1,
            "Quantity": 2
        },
        {
            "InvoiceItemId": 2,
            "InvoiceId": 1,
            "Quantity": 3
        }
    ])

    def test_1():
        # Set expected result
        expected = [{
            "InvoiceId": 1,
            "Quantity": 5
        }]

        # Call the transform we are testing with our mocks
        # Note that we use rafa.temp() instead of rafa.transform() so that the output table is temporary
        t_invoices = rafa.temp_transform(self, sources={"invoices": mock_src_invoices, "invoice_items": mock_src_invoice_items})
        
        assert rafa.select_all(t_invoices).to_dict('records') == expected

    test_1()
        