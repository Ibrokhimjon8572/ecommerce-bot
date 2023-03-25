import uuid

from django.db import models


# Create your models here.
class User(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)
    language = models.CharField(max_length=2, null=False, default='uz')
    user_id = models.CharField(max_length=20, null=False)
    username = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=False)
    name = models.CharField(max_length=30, null=True, blank=False)
    is_admin = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return self.name
