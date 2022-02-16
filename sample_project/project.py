from rafa import *
# TODO add imports

# Register sources
src_customers = rafa.source('customers')
src_employees = rafa.source('employees')
src_invoices = rafa.source('invoices')
src_invoice_items = rafa.source('invoice_items')

# Create revenue tables
invoices = rafa.transform(invoices, sources={"invoices": src_invoices, "invoice_items": src_invoice_items})
monthly_revenue = rafa.transform(revenue, name='monthly_revenue', period='month', sources={"invoices": src_invoices, "invoice_items": src_invoice_items})
weekly_revenue = rafa.transform(revenue, name='weekly_revenue', period='week', sources={"invoices": src_invoices, "invoice_items": src_invoice_items})

# Create employee revenue table - transforms can be dynamic based on inputs
customers = rafa.transform(customers, sources={"customers": src_customers})
monthly_revenue_by_support_rep = rafa.transform(revenue, sources={"invoices": invoices, "customers": customers, "employees": src_employees}, name='monthly_revenue_by_support_rep', period='month')

# TODO should wee include any select statements?