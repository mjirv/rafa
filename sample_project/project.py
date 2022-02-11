from rafa import *
# TODO add imports

# Register sources
src_invoice_items = rafa.source('invoice_items')
src_customers = rafa.source('customers')
src_employees = rafa.source('employees')
src_invoices = rafa.source('invoices')
src_invoice_items = rafa.source('invoice_items')

# Create revenue tables
invoices = rafa.transform(invoices, sources={src_invoices, src_invoice_items})
monthly_revenue = rafa.transform(revenue, name='monthly_revenue', period='month')
weekly_revenue = rafa.transform(revenue, name='weekly_revenue', period='week')

# Create employee revenue table - transforms can be dynamic based on inputs
customers = rafa.transform(customers, sources={src_customers})
monthly_revenue_by_support_rep = rafa.transform(revenue, sources={invoices, customers, src_employees}, name='monthly_revenue_by_support_rep', period='month')

# TODO should wee include any select statements?