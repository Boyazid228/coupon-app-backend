from django.db import models
from django.conf import settings
from categories.models import *


class Order(models.Model):
    STATUS_CHOICES = [
        ("accepted", "Accepted"),
        ("denied", "Denied"),
        ("ready", "Payed"),
    ]

    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="orders_as_user")
    payment = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="accepted")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders_as_owner")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        user_name = self.user.email if self.user else "Unknown User"
        product_name = self.product.name if self.product else "Unknown Product"
        return f"{user_name} | {product_name}"
