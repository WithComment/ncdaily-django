from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string


def send_notices():
  from app.util import get_notices

  meetings, general = get_notices()
  notices = []

  for notice in meetings:
    tmp = {}
    tmp['subject'] = notice['Subject']
    tmp['level'] = notice['Level']
    tmp['teacher'] = notice['Teacher']
    tmp['details'] = []
    tmp['details'].append(notice.get('DateMeet'))
    tmp['details'].append(notice.get('TimeMeet'))
    tmp['details'].append(notice.get('PlaceMeet'))
    tmp['body'] = notice['Body']
    notices.append(tmp)

  for notice in general:
    tmp = {}
    tmp['subject'] = notice['Subject']
    tmp['level'] = notice['Level']
    tmp['teacher'] = notice['Teacher']
    tmp['body'] = notice['Body']
    notices.append(tmp)

  notices_mail = render_to_string('app/emails/notices.html', {
    'quote': '',
    'new_notices': notices,
    'old_notices': []
  })

  print(send_mail(
    subject='Test email',
    message=repr(notices),
    html_message=notices_mail,
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=['zhangj@newlands.school.nz']
  ))

def send_unsub_email(email: str):
  