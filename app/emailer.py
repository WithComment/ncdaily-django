from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from app.models import Subscriber


def send_notices():
  '''
  Send notices email to subscribers
  '''
  from app.utils import compare_notices, get_qod

  new, old = compare_notices()
  
  print(f'There are {len(new) + len(old)} notices today.')
  
  qod = get_qod()

  notices_mail = render_to_string('app/emails/notices.html', {
    'quote': qod,
    'new_notices': new,
    'old_notices': old
  })

  count = send_mail(
    subject='Test email',
    message=str(new) + str(old),
    html_message=notices_mail,
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=['zhangj@newlands.school.nz']
  )

  print(f'{count} notice emails sent.')


def send_unsub_mail(email: str):
  '''
  Send unsubscibe code to @param email.
  '''
  try:
    subscriber = Subscriber.objects.get(email=email)
    unsub_mail = render_to_string('app/emails/unsub.html', {
      'unsub_code': subscriber.unsub_code
    })

    send_mail(
      subject='Test unsub',
      message=subscriber.unsub_code,
      html_message=unsub_mail,
      from_email=settings.EMAIL_HOST_USER,
      recipient_list=[email]
    )
  
  except Subscriber.DoesNotExist:
    return

