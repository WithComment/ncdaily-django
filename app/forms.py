from django.forms import ModelForm

from app.models import Subscriber


class SubscribeForm(ModelForm):
  class Meta:
    model = Subscriber
    fields = ['email']


class UnsubscribeForm(ModelForm):
  class Meta:
    model = Subscriber
    fields = ['unsubscribe_code']