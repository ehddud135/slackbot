from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Inspector(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomerInspector(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class AndroidOption(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

class iOSOption(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

class Package(models.Model):
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=10)  # 'Android' or 'iOS'
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'platform', 'customer']

class AndroidResult(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    option = models.ForeignKey(AndroidOption, on_delete=models.CASCADE)
    result = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

class iOSResult(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    option = models.ForeignKey(iOSOption, on_delete=models.CASCADE)
    result = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

class InspectionRecord(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    inspection_date = models.DateTimeField()
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
