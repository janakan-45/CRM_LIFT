from django.db import models
from authentication.models import Item   # ✅ Item should be from inventory app
from authentication.models import CustomUser  # ✅ Replace Employee with CustomUser
from sales.models import Customer
from amc.models import AMC


##################################### Requisition Model ##########################################
class Requisition(models.Model):
    reference_id = models.CharField(max_length=10, unique=True, editable=False)
    date = models.DateField()
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.IntegerField()
    site = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='requisitions')
    amc_id = models.ForeignKey(AMC, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.CharField(max_length=100, blank=True)
    employee = models.ForeignKey(   # ✅ changed from Employee to CustomUser
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'SALESMAN'}  # ✅ restrict only SALESMAN
    )
    status = models.CharField(
        max_length=20,
        choices=[('OPEN', 'Open'), ('CLOSED', 'Closed')],
        default='OPEN'
    )
    approve_for = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')],
        default='PENDING'
    )

    def save(self, *args, **kwargs):
        if not self.reference_id:
            last_requisition = Requisition.objects.all().order_by('id').last()
            if last_requisition:
                last_id = int(last_requisition.reference_id.replace('REQ', ''))
                self.reference_id = f'REQ{str(last_id + 1).zfill(3)}'
            else:
                self.reference_id = 'REQ001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference_id
