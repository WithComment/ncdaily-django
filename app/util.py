from datetime import date
import os

import requests
import xmltodict

def get_notices(
  y=date.today().year,
  m=date.today().month,
  d=date.today().day
) -> dict[str, list[dict]]:
  '''
  Get notices using Kamar API.
  Return a dictionary of (type, list of notices)
  where types are 'meeting' and 'general'.
  https://documenter.getpostman.com/view/1593669/
  '''

  # Request config.
  URL = 'https://parents.newlands.school.nz/api/api.php'
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'NCdaily',
    'Origin': 'file://',
    'X-Requested-With': 'nz.co.KAMAR'
  }

  # Credentials for logging in.
  USERNAME = os.environ.get('email').split('@')[0]
  PASSWORD = os.environ.get('password')

  # Login using credentials to get auth key.
  data = f'Command=Logon&Key=vtku&Username={USERNAME}&Password={PASSWORD}'
  r = requests.request("POST", URL, headers=headers, data=data)
  logon_results = xmltodict.parse(r.content)['LogonResults']
  key = logon_results['Key']

  # Get notices of y-m-d
  data = f'Command=GetNotices&Key={key}&Date={d}%2F{m}%2F{y}&ShowAll=YES'
  r = requests.request('POST', URL, headers=headers, data=data)
  result = (
    xmltodict.parse(r.content)
    .get('NoticesResults')
  )

  meetings = result.get('MeetingNotices', {}).get('Meeting')
  general = result.get('GeneralNotices', {}).get('General')

  return {
    'meetings': meetings,
    'general': general
  }