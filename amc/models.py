from django.db import models
from sales.models import Customer  # Assuming sales app has Customer model
from django.utils import timezone
from authentication.models import Item   
from datetime import timedelta

####################################amc/models.py####################################   

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
    amcname = models.CharField(max_length=100, blank=True)  # New field for AMC name
    invoice_frequency = models.CharField(
        max_length=20,
        choices=[
          ('annually', 'Annually'),
            ('semi_annually', 'Semi Annually'),
            ('quarterly', 'Quarterly'),
            ('monthly', 'Monthly'),
            ('per_service', 'Per Service')
        ],
        default='annually'
    )
    amc_type = models.ForeignKey(AMCType, on_delete=models.SET_NULL, null=True, blank=True)
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    #uploads_files = models.FileField(upload_to='amc_uploads/', null=True, blank=True, max_length=100)
    equipment_no = models.CharField(max_length=50, blank=True,null=True)
    notes = models.TextField(blank=True, null=True)
    is_generate_contract = models.BooleanField(default=False)
    no_of_services = models.IntegerField(default=12,blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,blank=True,null=True)
    no_of_lifts = models.IntegerField(default=0,blank=True,null=True)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00,blank=True,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False,blank=True,null=True)
    contract_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False,blank=True,null=True)
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,blank=True,null=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False,blank=True,null=True)
    amc_service_item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('expired', 'Expired'),
            ('cancelled', 'Cancelled'),
            ('on_hold', 'On Hold')
        ],
        default='active'
    )
    created = models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        if not self.reference_id:
            last_amc = AMC.objects.all().order_by('id').last()
            if last_amc:
                last_id = int(last_amc.reference_id.replace('AMC', ''))
                self.reference_id = f'AMC{str(last_id + 1).zfill(2)}'
            else:
                self.reference_id = 'AMC01'
    
        if self.is_generate_contract:
            from decimal import Decimal
            self.total = Decimal(str(self.price)) * Decimal(str(self.no_of_lifts)) * (Decimal('1') + Decimal(str(self.gst_percentage)) / Decimal('100'))
    
        self.contract_amount = self.total
    
        # Ensure total_amount_paid is properly initialized (default is 0.00)
        if not hasattr(self, 'total_amount_paid') or self.total_amount_paid is None:
            self.total_amount_paid = Decimal('0.00')
    
        # Calculate amount_due with proper decimal handling
        self.amount_due = Decimal(str(self.contract_amount)) - Decimal(str(self.total_amount_paid))

        # Determine status based on dates and payments
        today = timezone.now().date()
        if self.start_date > today:
            self.status = 'on_hold'
        elif self.start_date <= today <= self.end_date:
            if self.amount_due <= Decimal('0'):
                self.status = 'active'
            else:
                self.status = 'active'
        elif today > self.end_date:
            self.status = 'expired'

        # Update Customer's no_of_lifts and contracts if is_generate_contract is True
        if self.is_generate_contract:
            customer = self.customer
            customer.no_of_lifts = self.no_of_lifts
            customer.contracts = AMC.objects.filter(customer=customer, is_generate_contract=True).count()
            customer.save()

    def save(self, *args, **kwargs):
        if self.start_date and not self.end_date:
            self.end_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)

        super().save(*args, **kwargs)