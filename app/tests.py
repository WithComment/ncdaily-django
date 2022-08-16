import copy
from datetime import date
from io import StringIO
import json
import os
import sys
import time

from django.test import TestCase
from django.conf import settings
from django.core.management import call_command

# Create your tests here.
class CLISetTermDatesTest(TestCase):

  def test_current_year(self):

    old_stdin = sys.stdin
    sys.stdin = StringIO()
    filename = 'test_term_dates.json'
    cur_year = date.today().year
    expected = {
      str(cur_year): {},
      str(cur_year + 1): {}
    }
    test = []

    # Create expected term dates for Term t Year y.
    def create_expected(exp, y, t):
      start = f'{y}-0{t}-01'
      end = f'{y}-0{t}-02'
      exp[str(y)][str(t)] = {
        'start': start,
        'end': end
      }

    # Create test input and expected input.
    for i in range(1, 5):
      create_expected(expected, cur_year, i)
      create_expected(expected, cur_year + 1, i)
      test.extend([f'{i}-1\n', f'{i}-2\n'])
    test *= 2
    sys.stdin.writelines(test)

    # Write to test file using stdin.
    call_command('set_term_dates', F=filename)
    call_command('set_term_dates', Y=[(cur_year + 1)], F=filename)

    # Prevent unexpected behaviours.
    sys.stdin = old_stdin

    # Construct filepath of the test file.
    filepath = os.path.join(
      settings.BASE_DIR,
      'app', 'static', filename
    )

    # Assert content of test file is expected.
    with open(filepath) as f:
      self.assertDictEqual(json.load(f), expected)

    # Delete the test file.
    os.remove(filepath)