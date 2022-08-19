from django.db import models

class Subscriber(models.Model):
  email = models.EmailField(max_length=254, unique=True)
  unsub_code = models.CharField(max_length=6, null=True, blank=True)

  def __str__(self):
    return self.email


class Notice(models.Model):
  date = models.DateField(auto_now=False, auto_now_add=False, unique=True)
  notices = models.JSONField()