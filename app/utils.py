'''
Contains functions that interact with third-party APIs.
Include getting notices from Kamar API (https://documenter.getpostman.com/view/1593669/)
and getting quote of the day from https://quotes.rest.
'''
from datetime import date as dt, timedelta
import json
import os
from typing import Any, Dict, List, Set, Tuple

from django.db import IntegrityError
from django.utils import timezone
import requests
import xmltodict

from app.models import Notice

# Request config. See Kamar API documentation for more details.
URL = 'https://parents.newlands.school.nz/api/api.php'
HEADERS = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'User-Agent': 'NCdaily',
  'Origin': 'file://',
  'X-Requested-With': 'nz.co.KAMAR'
}


class BaseNotice():

  def __init__(
    self,
    notice: Dict[str, str]
  ) -> None:
    self.subject = notice['Subject']
    self.body = notice['Body']
    self.level = notice['Level']
    self.teacher = notice['Teacher']
    self.details = []
    if 'DateMeet' in notice:
      self.details.append(notice['DateMeet'])
      self.details.append(notice['TimeMeet'])
      self.details.append(notice['PlaceMeet'])
  

  def __hash__(self) -> int:
    return hash(self.body)
  

  def __eq__(self, __o: object) -> bool:
    return (
      isinstance(__o, BaseNotice) and
      self.subject == __o.subject and
      self.body == __o.body
    )
  

  def __str__(self) -> str:
    return f'{self.subject}: {self.body}'
  

  def serialize(self) -> Dict[str, Any]:
    return vars(self)


def get_auth_key() -> str:
  '''
  Get auth key in order to use the API.
  '''
  # Credentials for logging in.
  # The part of the email in front of @ is the username.
  USERNAME = os.environ['email'].split('@')[0]
  PASSWORD = os.environ['password']

  # Login to Kamar API using credentials to get auth key.
  data = f'Command=Logon&Key=vtku&Username={USERNAME}&Password={PASSWORD}'
  r = requests.request("POST", URL, headers=HEADERS, data=data)
  logon_results = xmltodict.parse(r.content)['LogonResults']

  return logon_results['Key']


def get_notices(
  date: dt = timezone.localdate()
) -> requests.Response:
  '''
  Get notices using Kamar API.
  https://documenter.getpostman.com/view/1593669/
  '''
  key = get_auth_key()
  # Get notices of yyyy-mm-dd
  data = f'Command=GetNotices&Key={key}&Date={date.day}%2F{date.month}%2F{date.year}&ShowAll=YES'
  r = requests.request('POST', URL, headers=HEADERS, data=data)

  return r


def parse_notices(
  date: dt = timezone.localdate()
) -> List[Dict[str, Any]]:
  '''
  Parse the response to a list of notices.
  '''
  response = get_notices(date)
  result = xmltodict.parse(response.content)

  # Extract only notice contents.
  # Use dict.get() instead of key to prevent exceptions.
  result = result.get('NoticesResults', {})
  meetings = (
    result.get('MeetingNotices', {})
    .get('Meeting', [])
  )
  general = (
    result.get('GeneralNotices', {})
    .get('General', [])
  ) 

  # In the case where there is only one notice, convert to list.
  if meetings and not isinstance(meetings, list):
    meetings = [meetings]
  if general and not isinstance(general, list):
    general = [general]

  return meetings + general


def save_notices(
  date: dt = timezone.localdate(),
  overwrite: bool = False
) -> None:
  '''
  Save the notices of @param date to database.
  Return the notices saved.
  '''
  notices = parse_notices(date)
  try:
    # Create notice of that day.
    Notice.objects.create(date=date, notices=notices)
  except IntegrityError:
    # If the notice of that day already exist.
    print(f'Notices of {date.isoformat()} already exist.')
    if overwrite:
      print('Overwriting...')
      obj = Notice.objects.get(date=date)
      obj.notices = notices
      obj.save()
    else:
      print('Operation cancelled.')


def read_notices(
  date: dt = timezone.localdate()
) -> Set[BaseNotice]:
  '''
  Read notices from the database,
  convert to a set of GeneralNotice or MeetingNotice objects.
  '''

  notices = Notice.objects.get(date=date).notices
  result = set()
  for n in notices:
    print(n)
    result.add(BaseNotice(n))
  
  return result


def compare_notices(
  date1: dt = timezone.localdate(),
  date2: dt = timezone.localdate() - timedelta(1)
) -> Tuple[Set[BaseNotice], Set[BaseNotice]]:
  '''
  Compare the notices of @param day1 and @param day2.
  Return the new notices of day1.
  '''
  new = []
  old = []

  # Make sure that the notices of the dates exist.
  if not Notice.objects.filter(date=date1).exists():
    save_notices(date1)
  if not Notice.objects.filter(date=date2).exists():
    save_notices(date2)

  notices1 = read_notices(date1)
  notices2 = read_notices(date2)
  
  new = notices1 - notices2
  old = notices1 & notices2

  return new, old


def get_qod(**kwargs) -> Dict[str, str] | None:
  '''
  Get quote of the day from https://quotes.rest.
  '''
  URL = 'https://quotes.rest/qod'
  headers = {
    'Accept': 'application/json'
  }
  r = requests.request('GET', URL, params=kwargs, headers=headers)
  response = json.loads(r.content)
  quote = response.get('contents', {}).get('quotes', [])[0]

  if quote:
    return {
      'author': quote['author'],
      'quote': quote['quote']
    }
  else:
    print('Something went wrong.')
