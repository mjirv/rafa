from rafa import *
from transforms import customers, invoices, revenue

# Register sources
src_customers = rafa.source('customers')
src_employees = rafa.source('employees')
src_invoices = rafa.source('invoices')
src_invoice_items = rafa.source('invoice_items')
revenue_sources = {"invoices": src_invoices, "invoice_items": src_invoice_items}

m_customers = rafa.transform(customers, sources={"customers": src_customers})

# Create revenue tables
m_invoices = rafa.transform(invoices, sources=revenue_sources)
m_monthly_revenue = rafa.transform(revenue, name='monthly_revenue', period='month', sources=revenue_sources)
m_weekly_revenue = rafa.transform(revenue, name='weekly_revenue', period='week', sources=revenue_sources)

# Create employee revenue table - transforms can be dynamic based on inputs
m_monthly_revenue_by_support_rep = rafa.transform(revenue, sources={"invoices": m_invoices, "customers": m_customers, "employees": src_employees}, name='monthly_revenue_by_support_rep', period='month')

# TODO should wee include any select statements?