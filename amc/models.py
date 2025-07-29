from django.db import models
from sales.models import Customer  # Assuming sales app has Customer model
from django.utils import timezone

class AMCType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class PaymentTerms(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class AMC(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=10, unique=True, editable=False)
    invoice_frequency = models.CharField(
        max_length=20,
        choices=[
            ('annually', 'Annually'),
            ('semi_annually', 'Semi Annually'),
            ('quarterly', 'Quarterly'),
            ('monthly', 'Monthly'),
            ('weekly', 'Weekly'),
            ('every_other_weekly', 'Every Other Weekly')
        ],
        default='annually'
    )
    amc_type = models.ForeignKey(AMCType, on_delete=models.SET_NULL, null=True, blank=True)
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    uploads_files = models.FileField(upload_to='amc_uploads/', null=True, blank=True, max_length=100)
    equipment_no = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    is_generate_contract = models.BooleanField(default=False)
    no_of_services = models.IntegerField(default=12)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    no_of_lifts = models.IntegerField(default=0)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    status = models.CharField(max_length=20, default='Pending')

    def save(self, *args, **kwargs):
        if not self.reference_id:
            last_amc = AMC.objects.all().order_by('id').last()
            if last_amc:
                last_id = int(last_amc.reference_id.replace('AMC', ''))
                self.reference_id = f'AMC{str(last_id + 1).zfill(2)}'
            else:
                self.reference_id = 'AMC01'
        if self.is_generate_contract:
            self.total = self.price * self.no_of_lifts * (1 + self.gst_percentage / 100)

        # Determine status based on dates
        today = timezone.now().date()
        if self.start_date > today:
            self.status = 'Pending'
        elif self.start_date <= today <= self.end_date:
            self.status = 'Active'
        elif today > self.end_date:
            self.status = 'Overdue'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_id} - {self.customer.customer_id}"