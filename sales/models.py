from django.db import models
from datetime import timedelta, date
##########################################3Customer Model#########################################
# Dynamic dropdown models
class Route(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value

class Branch(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value

class ProvinceState(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value

# Sector choices
SECTOR_CHOICES = (
    ('government', 'Government'),
    ('private', 'Private'),
)

class Customer(models.Model):
    reference_id = models.CharField(max_length=10, unique=True, editable=False)
    site_id = models.CharField(max_length=30)   # Added Site ID
    job_no = models.CharField(max_length=50, blank=True)
    site_name = models.CharField(max_length=100)
    site_address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    office_address = models.TextField(blank=True)
    contact_person_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True)
    pin_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100)
    province_state = models.ForeignKey(ProvinceState, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=100)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES, default='private')
    routes = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    handover_date = models.DateField(null=True, blank=True)
    billing_name = models.CharField(max_length=100, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)
    gst_number = models.CharField(max_length=15, blank=True)
    # Mobile fields (Active and Expired)
    active_mobile = models.IntegerField(default=0)  # Number of active mobile entries
    expired_mobile = models.IntegerField(default=0)  # Number of expired mobile entries
    # Contracts field
    contracts = models.IntegerField(default=0)  # Number of contracts
    # No. of Lifts field
    no_of_lifts = models.IntegerField(default=0)  # Number of lifts
    # Service-related fields
    completed_services = models.IntegerField(default=0)
    due_services = models.IntegerField(default=0)
    overdue_services = models.IntegerField(default=0)
    # Tickets field
    tickets = models.IntegerField(default=0)
    lifts = models.ManyToManyField('authentication.Lift', blank=True)

    uploads_files = models.FileField(upload_to='customer_uploads/', null=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.reference_id:
            # Auto-generate reference_id (e.g., CUST001, CUST002, etc.)
            last_customer = Customer.objects.all().order_by('id').last()
            if last_customer:
                last_id = int(last_customer.reference_id.replace('CUST', ''))
                self.reference_id = f'CUST{str(last_id + 1).zfill(3)}'
            else:
                self.reference_id = 'CUST001'
        super().save(*args, **kwargs)

    @property
    def customer_id(self):
        """Backward compatible property to return the id"""
        return self.id


######################################## Quotation model#########################################

from amc.models import AMCType
from authentication.models import  Lift

class Quotation(models.Model):
    REFERENCE_PREFIX = 'ALQ'
    reference_id = models.CharField(max_length=10, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    amc_type = models.ForeignKey(AMCType, on_delete=models.SET_NULL, null=True, blank=True)
    sales_service_executive = models.ForeignKey('authentication.Employee', on_delete=models.SET_NULL, null=True, blank=True)
    lifts = models.ManyToManyField(Lift)
    type = models.CharField(
        max_length=50,
        choices=[
            ('Parts/Peripheral Quotation', 'Parts/Peripheral Quotation'),
            ('Repair', 'Repair'),
            ('AMC Renewal Quotation', 'AMC Renewal Quotation'),
            ('AMC', 'AMC')
        ],
        default='Parts/Peripheral Quotation'
    )
    year_of_make = models.CharField(max_length=4, blank=True)
    date = models.DateField(auto_now_add=True)
    remark = models.TextField(blank=True)
    other_remark = models.TextField(blank=True)
    uploads_files = models.FileField(upload_to='quotation_uploads/', null=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.reference_id:
            last_quotation = Quotation.objects.all().order_by('id').last()
            self.reference_id = f'{self.REFERENCE_PREFIX}{str(1000 + (last_quotation.id + 1) if last_quotation else 1001)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference_id
    

from authentication.models import Item


######################################## Invoice & InvoiceItem ##################################
class Invoice(models.Model):
    REFERENCE_PREFIX = 'INV'
    reference_id = models.CharField(max_length=10, unique=True, editable=False)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    amc_type = models.ForeignKey(AMCType, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    due_date = models.DateField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    payment_term = models.CharField(
        max_length=10,
        choices=[
            ('cash', 'Cash'),
            ('cheque', 'Cheque'),
            ('neft', 'NEFT')
        ],
        default='cash'
    )
    uploads_files = models.FileField(upload_to='invoice_uploads/', null=True, blank=True, max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ('open', 'Open'),
            ('paid', 'Paid'),
            ('partially_paid', 'Partially Paid')
        ],
        default='open'
    )

    def save(self, *args, **kwargs):
        if not self.reference_id:
            last_invoice = Invoice.objects.all().order_by('id').last()
            if last_invoice:
                last_id = int(last_invoice.reference_id.replace('INV', ''))
                self.reference_id = f'{self.REFERENCE_PREFIX}{str(last_id + 1).zfill(3)}'
            else:
                self.reference_id = 'INV001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference_id


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField(default=1)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total = self.rate * self.qty * (1 + (self.tax / 100))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Item for {self.invoice.reference_id}"


######################################## Recurring Invoice ######################################
class RecurringInvoice(models.Model):
    REFERENCE_PREFIX = 'RINV'
    reference_id = models.CharField(max_length=10, unique=True, editable=False)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    profile_name = models.CharField(max_length=100)
    order_number = models.CharField(max_length=50, blank=True)
    repeat_every = models.CharField(
        max_length=20,
        choices=[
            ('week', 'Week'),
            ('2week', '2 Weeks'),
            ('month', 'Month'),
            ('2month', '2 Months'),
            ('3month', '3 Months'),
            ('6month', '6 Months'),
            ('year', 'Year'),
            ('2year', '2 Years'),
        ],
        default='month'
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_generated_date = models.DateField(null=True, blank=True)
    sales_person = models.ForeignKey('authentication.Employee', on_delete=models.SET_NULL, null=True, blank=True)
    billing_address = models.TextField(blank=True)
    gst_treatment = models.CharField(max_length=50, blank=True)
    uploads_files = models.FileField(upload_to='recurring_invoice_uploads/', null=True, blank=True, max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='active'
    )

    def save(self, *args, **kwargs):
        if not self.reference_id:
            last_invoice = RecurringInvoice.objects.all().order_by('id').last()
            if last_invoice:
                last_id = int(last_invoice.reference_id.replace('RINV', ''))
                self.reference_id = f'{self.REFERENCE_PREFIX}{str(last_id + 1).zfill(3)}'
            else:
                self.reference_id = 'RINV001'
        if self.customer and not self.billing_address:
            self.billing_address = self.customer.site_address
        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference_id

    # Utility methods for scheduling
    def get_next_date(self):
        if not self.last_generated_date:
            return self.start_date
        mapping = {
            'week': 7,
            '2week': 14,
            'month': 30,
            '2month': 60,
            '3month': 90,
            '6month': 180,
            'year': 365,
            '2year': 730,
        }
        return self.last_generated_date + timedelta(days=mapping[self.repeat_every])

    def should_generate(self, today=None):
        today = today or date.today()
        next_date = self.get_next_date()
        if self.end_date and next_date > self.end_date:
            return False
        return today >= next_date


class RecurringInvoiceItem(models.Model):
    recurring_invoice = models.ForeignKey(RecurringInvoice, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField(default=1)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total = self.rate * self.qty * (1 + (self.tax / 100))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Item for {self.recurring_invoice.reference_id}"



#########################################paynment received###########################################

class PaymentReceived(models.Model):
    REFERENCE_PREFIX = 'PAY'
    payment_number = models.CharField(max_length=10, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)  # Linked to particular invoice for deposit consideration
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Temporarily used as 'value' since no dedicated amount field exists in Invoice
    date = models.DateField()
    payment_type = models.CharField(
        max_length=20,
        choices=[
            ('cash', 'Cash'),
            ('bank_transfer', 'Bank Transfer')
        ],
        default='cash'
    )
    tax_deducted = models.CharField(
        max_length=20,
        choices=[
            ('no', 'No Tax deducted'),
            ('yes_tds', 'Yes, TDS (Income Tax)')
        ],
        default='no'
    )
    uploads_files = models.FileField(upload_to='payment_received_uploads/', null=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.payment_number:
            last_payment = PaymentReceived.objects.all().order_by('id').last()
            if last_payment:
                last_id = int(last_payment.payment_number.replace('PAY', ''))
                self.payment_number = f'{self.REFERENCE_PREFIX}{str(last_id + 1).zfill(3)}'
            else:
                self.payment_number = 'PAY001'
        # No automatic TDS calculation implemented yet, as Invoice lacks an amount field and TDS rate is unspecified.
        # If tax_deducted == 'yes_tds', the amount is treated as received value; future enhancements can add TDS computation based on invoice details.
        super().save(*args, **kwargs)

    def __str__(self):
        return self.payment_number

