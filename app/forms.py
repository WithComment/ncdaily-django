from typing import Dict, Any

from django.forms import EmailField, ModelForm

from app.models import Subscriber

class SubscribeForm(ModelForm):
  email = EmailField()
  class Meta:
    model = Subscriber
    fields = ['email']

  def clean(self) -> Dict[str, Any]:
    '''
    Override the clean method to bypass uniqueness check.
    Django defaults to performing uniqueness check on model instance
    create by ModelForm which in this case is not desired.
    '''
    cleaned_data = self.cleaned_data
    return cleaned_data


class UnsubscribeForm(ModelForm):
  class Meta:
    model = Subscriber
    fields = ['unsub_code']