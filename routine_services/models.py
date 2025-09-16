from django.db import models
from authentication.models import Lift, Employee
from sales.models import Customer, Route

class RoutineService(models.Model):
    STATUS_CHOICES = [
        ('due', 'Due'),
        ('complete', 'Complete'),
    ]

    lift = models.ForeignKey(Lift, on_delete=models.CASCADE, related_name='routine_services')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='routine_services')
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

    service_date = models.DateField()
    no_of_services = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='due')

    cust_location = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.cust_location and self.customer:
            self.cust_location = self.customer.site_address
        if not self.route and self.customer:
            self.route = self.customer.routes
        super().save(*args, **kwargs)

    @property
    def gmap_url(self):
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        return f"https://www.google.com/maps/search/?api=1&query={self.cust_location}"

    def __str__(self):
        return f"{self.lift.lift_code} - {self.customer.site_name}"
