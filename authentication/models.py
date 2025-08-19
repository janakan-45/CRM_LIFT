from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User



#############################lift########################################
class FloorID(models.Model):
    value = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.value

class Brand(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value

class MachineType(models.Model):
    value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.value

class MachineBrand(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value

class DoorType(models.Model):
    value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.value

class DoorBrand(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value

class LiftType(models.Model):
    value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.value

class ControllerBrand(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value

class Cabin(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value

class Lift(models.Model):
    lift_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    floor_id = models.ForeignKey(FloorID, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    model = models.CharField(max_length=100)
    no_of_passengers = models.CharField(max_length=50)
    load_kg = models.CharField(max_length=50)
    speed = models.CharField(max_length=50)
    lift_type = models.ForeignKey(LiftType, on_delete=models.SET_NULL, null=True)
    machine_type = models.ForeignKey(MachineType, on_delete=models.SET_NULL, null=True)
    machine_brand = models.ForeignKey(MachineBrand, on_delete=models.SET_NULL, null=True)
    door_type = models.ForeignKey(DoorType, on_delete=models.SET_NULL, null=True)
    door_brand = models.ForeignKey(DoorBrand, on_delete=models.SET_NULL, null=True)
    controller_brand = models.ForeignKey(ControllerBrand, on_delete=models.SET_NULL, null=True)
    cabin = models.ForeignKey(Cabin, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.lift_code
    



################################items########################################

from django.db import models

class Type(models.Model):
    value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.value

class Make(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value

class Unit(models.Model):
    value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.value

class Item(models.Model):
    item_number = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=100)
    make = models.ForeignKey(Make, on_delete=models.SET_NULL, null=True)
    model = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    capacity = models.CharField(max_length=50)
    threshold_qty = models.IntegerField(default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    service_type = models.CharField(max_length=10, choices=[('Goods', 'Goods'), ('Services', 'Services')], default='Goods')
    tax_preference = models.CharField(max_length=15, choices=[('Taxable', 'Taxable'), ('Non-Taxable', 'Non-Taxable')], default='Non-Taxable')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    sac_code = models.CharField(max_length=10, blank=True, null=True)
    #hsn_hac_code = models.CharField(max_length=10, blank=True, null=True)
    igst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True, null=True)
    gst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True, null=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.item_number:
            last_item = Item.objects.all().order_by('id').last()
            self.item_number = f'PART{str(1000 + (last_item.id + 1) if last_item else 1001)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.item_number



###########################complaints########################################


from sales.models import Customer

class Employee(models.Model):
    username = models.CharField(max_length=150, unique=True,blank=True,null=True)
    email = models.EmailField(unique=True,blank=True,null=True)
    password = models.CharField(max_length=128,null=True,blank=True)  # Stores hashed password
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Hash the password if it has been changed or is new
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        # Ensure name is derived from username if not provided
        if not self.name:
            self.name = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    REFERENCE_PREFIX = 'CMP'
    reference = models.CharField(max_length=10, unique=True, editable=False)
    type = models.CharField(max_length=50, choices=[
        ('Site Inspection', 'Site Inspection'),
        ('Spec Checking', 'Spec Checking'),
        ('Break Down Calls', 'Break Down Calls'),
        ('Service Request', 'Service Request'),
        ('New Installation', 'New Installation')
    ])
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    contact_person_name = models.CharField(max_length=100, blank=True)
    contact_person_mobile = models.CharField(max_length=15, blank=True)
    block_wing = models.CharField(max_length=50, blank=True)
    assign_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=[
        ('Urgent', 'Urgent'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    ], default='Medium')
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    customer_signature = models.TextField(blank=True)  # New field
    technician_remark = models.TextField(blank=True)  # New field
    technician_signature = models.TextField(blank=True)  # New field
    solution = models.TextField(blank=True)  # New field

    def save(self, *args, **kwargs):
        if not self.reference:
            last_complaint = Complaint.objects.all().order_by('id').last()
            self.reference = f'{self.REFERENCE_PREFIX}{str(1000 + (last_complaint.id + 1) if last_complaint else 1001)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference
    



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)