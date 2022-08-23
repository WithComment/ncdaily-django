import random

from django.shortcuts import redirect, render
from django.urls import reverse

import app.emailer as emailer
from app.forms import SubscribeForm, UnsubscribeForm
from app.models import Subscriber

# Create your views here.

DUPLICATE = "I know you like our app, but you can't sign up twice..."
EMPTY = "You haven't entered anything!"
INVALID_EMAIL = "The email you entered is invalid!"
DISABLED = "Sorry, the app is currently disabled right now. It will be up soon though..."
BLOCKED = "Please use your personal email address..."
NOT_SUBSCRIBED = "You can't unsubscribe if you haven't subscribed!"

def index(request):

  num_students = Subscriber.objects.count() // 10 * 10
  message = None
  
  if request.method == 'POST':
    # User submitted the subscription form

    form = SubscribeForm(request.POST)

    # Validate the form.
    if form.is_valid():
      Subscriber.objects.create(
        email=form.cleaned_data['email']
      )

      
    else:
      message = INVALID_EMAIL
  
  return render(request, 'app/home.html', {
    'message': message,
    'num_students': num_students,
  })


def about(request):
  return render(request, 'app/about.html')


def faq(request):
  return render(request, 'app/faq.html')


def unsubscribe(request):

  message = None

  if request.method == 'POST':
    # User submmitted the unsubscribe form.

    form = SubscribeForm(request.POST)
    
    # Validate the form.
    if form.is_valid():
      email = form.cleaned_data['email']
      try:
        subscriber = Subscriber.objects.get(email=email)
        subscriber.unsub_code = random.randint(100000, 999999)
        subscriber.save()

        request.session['email'] = email

        return redirect(reverse('cm_unsub'))

      except Subscriber.DoesNotExist:
        message = NOT_SUBSCRIBED
    
    else:
      message = INVALID_EMAIL
  
  return render(request, 'app/unsub.html', {
    'message': message
  })


def confirm_unsubscribe(request):
  email = request.session.get('email')
  if not email:
    return redirect(reverse('unsub'))
  
  if request.method == 'POST':
    form = UnsubscribeForm(request.POST)

    if form.is_valid():
      code = form.cleaned_data['unsub_code']
      print(code, email)

      try:
        # Get the subscriber using the email and the unsubscribe code.
        Subscriber.objects.get(
          email=email,
          unsub_code=code
        ).delete()

        # Remove email from session.
        request.session.pop('email')

        return render(request, 'app/farewell.html')
      
      except Subscriber.DoesNotExist:
        pass
  
  elif request.method == 'GET':
    emailer.send_unsub_mail(email)

  # GET request, invalid form or invalid credentials
  return render(request, 'app/confirm_unsubscribe.html', {
    'email': email
  })