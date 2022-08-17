from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    unsubscribe_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.email