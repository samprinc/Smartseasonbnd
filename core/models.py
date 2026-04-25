from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# 1. Define these once to reuse in both models
STAGE_CHOICES = [
    ('planted', 'Planted'),
    ('growing', 'Growing'),
    ('ready', 'Ready'),
    ('harvested', 'Harvested')
]

class User(AbstractUser):
    ROLE_CHOICES = (('admin', 'Admin'), ('agent', 'Field Agent'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Field(models.Model):
    name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=100)
    planting_date = models.DateField()
    # 2. Use the shared choices here
    stage = models.CharField(max_length=20, default='planted', choices=STAGE_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='fields')

    @property
    def current_status(self):
        last_update = self.updates.order_by('-created_at').first()
        if self.stage == 'harvested':
            return 'Completed'
        if last_update and (timezone.now() - last_update.created_at).days > 7:
            return 'At Risk'
        return 'Active'

class FieldUpdate(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='updates')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()
    # 3. Enforce the same choices here so the data is valid
    stage_at_update = models.CharField(max_length=20, choices=STAGE_CHOICES)