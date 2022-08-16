from datetime import date
import json
import os
from pathlib import Path
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):

  help = (
    '''
    Set the term dates.
    The date format should be mm-dd.
    '''
  )


  def add_arguments(self, parser) -> None:

    parser.add_argument(
      '-Y',
      nargs=1,
      type=int,
      default=[date.today().year],
      help='Specify the year to set.'
    )

    parser.add_argument(
      '-F',
      nargs=1,
      default='term_dates.json',
      help='Specify the json file to use.'
    )
  

  def construct_dates(self, year):
    '''
    Create term dates based on user input.
    '''
    terms = {}
    for i in range(1, 5):
      self.stdout.write(f'Term {i}:')

      while True:

        try:

          # Output the prompt, then get input.
          self.stdout.write('Start:')
          s = sys.stdin.readline()
          self.stdout.write('End:')
          e = sys.stdin.readline()

          if not (s and e):
            # EOF reached.
            return terms

          # Map the input to (day, month).
          s = tuple(map(int, s.split('-')))
          e = tuple(map(int, e.split('-')))

          # Construct the date
          s = date(year, s[0], s[1])
          e = date(year, e[0], e[1])

        except (ValueError, IndexError):
          self.stdout.write(self.style.ERROR(
            'Invalid date(s).'
          ))
          continue

        if not e > s:
          self.stdout.write(self.style.ERROR(
            'The end date must be later than the start date.'
          ))
          continue

        break
      
      # Set start and end dates for Term i
      terms[i] = {
        'start': s.isoformat(),
        'end': e.isoformat()
      }
    
    return terms


  def handle(self, *args, **options):

    # The json file should locate in ROOT/json
    dirpath = os.path.join(settings.BASE_DIR, 'json')
    filepath = os.path.join(dirpath, options['F'])

    year = options['Y'][0]
    all_years = {}

    if sys.stdin.seekable():
      # Using test input.
      sys.stdin.seek(0)

    # Create dir and file if not exist.
    os.makedirs(dirpath, exist_ok=True)
    Path(filepath).touch(exist_ok=True)

    # Load existing data.
    with open(filepath) as f:
      # If there is content in the file.
      if os.path.getsize(filepath) > 0:
        all_years = json.load(f)

    self.stdout.write(self.style.NOTICE(
      'Date format: mm-dd'
    ))

    # Write data back to the same file.
    all_years[str(year)] = self.construct_dates(year)
    with open(filepath, 'w') as f:
      json.dump(all_years, f)
    
    self.stdout.write(self.style.SUCCESS(
      f'Successfully set term dates for {year}.'
    ))