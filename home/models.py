from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Bag(models.Model):
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=120)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
