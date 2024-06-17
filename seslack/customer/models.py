from django.db import models


class CustomerList(models.Model):
    customer_name = models.CharField(max_length=30)
    manager = models.CharField(max_length=30)
