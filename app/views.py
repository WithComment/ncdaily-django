import random
from django.shortcuts import redirect, render
from django.urls import reverse

from app.forms import SubscribeForm, UnsubscribeForm
from app.models import Subscriber

# Create your views here.


def index(request):
  
  if request.method == 'POST':
    # User submitted the subscription form

    form = SubscribeForm(request.POST)

    # Validate the form.
    if form.is_valid():

      # Create a subscriber from form.
      subscriber = form.save(commit=False)

      # Set unsubscribe code.
      code = random.randint(100000, 999999)
      subscriber.unsubscribe_code = code

      # Save to database.
      subscriber.save()
  
  else:
    return render(request, 'app/home.html')


def about(request):
  return render(request, 'app/about.html')


def faq(request):
  return render(request, 'faq.html')


def unsubscribe(request):

  if request.method == 'POST':
    # User submmitted the unsubscribe form.

    form = SubscribeForm(request.POST)
    
    # Validate the form.
    if form.is_valid():
      request.session['email'] = form.cleaned_data['email']
      return redirect(reverse(confirm_unsubscribe))
  
  else:
    return render(request, 'app/unsub.html')


def confirm_unsubscribe(request):
  if request.method == 'POST':
    form = UnsubscribeForm(request.POST)

    if form.is_valid():
      code = form.cleaned_data['unsubscribe_code']

      try:
        # Get the subscriber using the email and the unsubscribe code.
        Subscriber.objects.get(
          email=request.session['email'],
          unsubscribe_code=code
        ).delete()

        # Remove email from session.
        request.session.pop('email')
        
        return render(request, 'app/farewell.html')
      
      except Subscriber.DoesNotExist:
        pass
  
  # GET request, invalid form or invalid credentials
  return render(request, 'app/confirm_unsubscribe.html')