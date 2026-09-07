from django.conf import settings
from django.db import models

from common.models import BaseModel



class Address(BaseModel):

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="addresses")

    label = models.CharField(max_length=50)

    recipient_name = models.CharField(max_length=150)

    phone = models.CharField(max_length=15)

    country = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    street = models.CharField(max_length=255)

    postal_code = models.CharField(max_length=20,blank=True)

    is_default = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id"],
                condition=models.Q(is_default=True),
                name="unique_default_address_per_user",
            )
        ]

    def __str__(self):
        return f"{self.label} - {self.recipient_name}"
