from pprint import pprint
from typing import Sequence

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from app.models import Subscriber
from app.utils import compare_notices, get_qod


def send_mass_html_mails(
  subject: str,
  body: str,
  recipients: Sequence[str]
) -> int:
  '''
  Send the same html email to multiple recipients.
  '''
  messages = EmailMultiAlternatives(
    subject=subject,
    body=body,
    to=recipients
  )
  messages.content_subtype = 'html'
  return messages.send()


def send_notices(
  recipients: str | list[str] = []
) -> int:
  '''
  Send notices email to subscribers
  '''

  # Get email content.
  new, old = compare_notices()
  print(f'{len(new) + len(old)} notices today, {len(new)} are new.')
  qod = get_qod()

  # E.g. Tuesday, Aug 23 - NC Notices
  subject = timezone.localdate().strftime('%A, %b %d - NC Notices')

  # Construct email body.
  body = render_to_string('app/emails/notices.html', {
    # 'quote': qod,
    'new_notices': new,
    'old_notices': old
  })

  if not recipients:
    recipients = (
      Subscriber.objects
      .values_list('email', flat=True)
    )

  if isinstance(recipients, str):
    recipients = [recipients]

  return send_mass_html_mails(
    subject=subject,
    body=body,
    recipients=recipients
  )


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

