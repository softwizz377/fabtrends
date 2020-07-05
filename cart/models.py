from django.db import models
from django.conf import settings
from fabtrendapp.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)

    class Meta:
        ordering = ['-timestamp']


# Create your models here.
