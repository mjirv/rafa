from rafa import *
from transforms import customers, invoices, revenue

### Configure database ###
rafa.config(debug=True)

### Run tests ###
rafa.test(invoices)

### Register sources ###
src_customers = rafa.source('Customer')
src_employees = rafa.source('Employee')
src_invoices = rafa.source('Invoice')
src_invoice_items = rafa.source('InvoiceLine')

### Run Transforms ###
# Create basic customers table
m_customers = rafa.transform(customers, sources={"customers": src_customers})

# Create revenue tables
m_invoices = rafa.transform(invoices, sources={"invoices": src_invoices, "invoice_items": src_invoice_items})
m_monthly_revenue = rafa.transform(revenue, name='monthly_revenue', period='month', sources={"invoices": m_invoices})
m_weekly_revenue = rafa.transform(revenue, name='weekly_revenue', period='week', sources={"invoices": m_invoices})

# Create employee revenue table - transforms can be dynamic based on inputs
revenue_by_support_rep = rafa.transform(
    revenue, 
    sources={"invoices": m_invoices, "customers": m_customers}, 
    join={"name": "customers", "on": "CustomerId"},
    groupByCols=['SupportRepId'],
    name='revenue_by_support_rep'
)
