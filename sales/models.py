from django.db import models

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
    site_id = models.CharField(max_length=10, unique=True)  # Added Site ID
    job_no = models.CharField(max_length=50, blank=True)
    site_name = models.CharField(max_length=100)
    site_address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    mobile_sms_notification = models.CharField(max_length=15, blank=True)
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

    def __str__(self):
        return self.reference_id