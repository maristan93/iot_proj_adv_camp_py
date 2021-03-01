from django.db import models


# Enable administrators to manage products. Each product will have at least a name, image, price and quantity on stock.
# Enable administrators to manage discounts. For example, administrator can define that Domaćica cookies are on 30%
# discount every Wednesday and Thursday from 19:00-21:00.
# Each discount should be associated with exactly one BLE beacon.


class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="product/image/", blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    quantity = models.DecimalField(decimal_places=0, max_digits=4)
    section = models.CharField(max_length=50)   # BLE beacon
    discount = models.DecimalField(decimal_places=0, max_digits=3)
    discountTimeStart = models.TimeField(blank=True, null=True)
    discountTimeEnd = models.TimeField(blank=True, null=True)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    repeat_discount = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DiscountItem(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="product/image/", blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    quantity = models.DecimalField(decimal_places=0, max_digits=4)

    def __str__(self):
        return self.name


class Survey(models.Model):
    service = models.DecimalField(decimal_places=0, max_digits=1)
    comment = models.TextField(blank=True, null=True)


