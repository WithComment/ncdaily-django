from django.db import models
from django.db.models.constraints import UniqueConstraint

class Subscriber(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    unsubscribe_code = models.CharField(max_length=6, null=True, blank=True)

    class Meta:
      constraints = [
        UniqueConstraint(fields=['email'], name='Unique email')
      ]

    def __str__(self):
        return self.email