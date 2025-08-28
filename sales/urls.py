from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    ##########################customer URLs########################################
    path('add-route/', views.add_route, name='add_route'),
    path('edit-route/<int:pk>/', views.edit_route, name='edit_route'),
    path('delete-route/<int:pk>/', views.delete_route, name='delete_route'),
    path('add-branch/', views.add_branch, name='add_branch'),
    path('edit-branch/<int:pk>/', views.edit_branch, name='edit_branch'),
    path('delete-branch/<int:pk>/', views.delete_branch, name='delete_branch'),
    path('add-province-state/', views.add_province_state, name='add_province_state'),
    path('edit-province-state/<int:pk>/', views.edit_province_state, name='edit_province_state'),
    path('delete-province-state/<int:pk>/', views.delete_province_state, name='delete_province_state'),
    path('routes/', views.get_routes, name='get_routes'),
    path('branches/', views.get_branches, name='get_branches'),
    path('province-states/', views.get_province_states, name='get_province_states'),
    # Customer CRUD URLs
    path('add-customer/', views.add_customer, name='add_customer'),
    path('customer-list/', views.customer_list, name='customer_list'),
    path('edit-customer/<int:pk>/', views.edit_customer, name='edit_customer'),
    path('delete-customer/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('export-customers/', views.export_customers_to_excel, name='export_customers_to_excel'),
    path('import-customers-csv/', views.import_customers_csv, name='import_customers_csv'),

##################################quotation########################################
     path('add-quotation/', views.add_quotation, name='add_quotation'),
    path('edit-quotation/<int:pk>/', views.edit_quotation, name='edit_quotation'),
    path('delete-quotation/<int:pk>/', views.delete_quotation, name='delete_quotation'),
    path('quotation-list/', views.quotation_list, name='quotation_list'),
    path('export-quotations-to-excel/', views.export_quotations_to_excel, name='export_quotations_to_excel'),



#################################invoice########################################

    path('add-invoice/', views.add_invoice, name='add_invoice'),
    path('edit-invoice/<int:pk>/', views.edit_invoice, name='edit_invoice'),
    path('delete-invoice/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('invoice-list/', views.invoice_list, name='invoice_list'),
    path('export-invoices-to-excel/', views.export_invoices_to_excel, name='export_invoices_to_excel'),
    # urls.py (add this to urlpatterns, after invoice URLs)
    path('print-invoice/<int:pk>/', views.print_invoice, name='print_invoice'),


###########################################recurring invoice urls##########################################

    # Add the following to urls.py inside the urlpatterns list, after the invoice URLs

    path('add-recurring-invoice/', views.add_recurring_invoice, name='add_recurring_invoice'),
    path('edit-recurring-invoice/<int:pk>/', views.edit_recurring_invoice, name='edit_recurring_invoice'),
    path('delete-recurring-invoice/<int:pk>/', views.delete_recurring_invoice, name='delete_recurring_invoice'),
    path('recurring-invoice-list/', views.recurring_invoice_list, name='recurring_invoice_list'),
    path('export-recurring-invoices-to-excel/', views.export_recurring_invoices_to_excel, name='export_recurring_invoices_to_excel'),
    path('generate_invoice_from_recurring/<str:pk>/', views.generate_invoice_from_recurring, name='generate_invoices_from_recurring'),





############################################payment received urls##########################################

    path('add-payment-received/', views.add_payment_received, name='add_payment_received'),
    path('edit-payment-received/<int:pk>/', views.edit_payment_received, name='edit_payment_received'),
    path('delete-payment-received/<int:pk>/', views.delete_payment_received, name='delete_payment_received'),
    path('payment-received-list/', views.payment_received_list, name='payment_received_list'),
    path('export-payments-received-to-excel/', views.export_payment_received_to_excel, name='export_payments_received_to_excel'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)