import random
from django.shortcuts import redirect, render
from django.urls import reverse

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
  
  return render(request, 'app/home.html', {
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
      if Subscriber.objects.filter(email=email).exists():
        request.session['email'] = email

        return redirect(reverse('cm_unsub'))
      else:
        message = NOT_SUBSCRIBED
    
    else:
      message = INVALID_EMAIL
  
  return render(request, 'app/unsub.html', {
    'message': message
  })


def confirm_unsubscribe(request):
  email = request.session['email']
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
  return render(request, 'app/confirm_unsubscribe.html', {
    'email': email
  })