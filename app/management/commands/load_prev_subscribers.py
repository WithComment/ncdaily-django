import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from app.models import Subscriber

class Command(BaseCommand):
    '''
    DO NOT USE THIS COMMAND!
    Only used by John at the beginning of this project 
    to migrate data from the database to the django model.
    '''

    help = (
        '''
        Load subscribers from a csv file. 
        This should only be used once in the project's lifetime
        '''
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            'filename',
            nargs='?',
            default='subscribers.csv',
            help='Specify the file to load.'
        )

    def handle(self, *args, **options):
    
        # The file should be located at the root directory.
        filepath = os.path.join(settings.BASE_DIR, options['filename'])
        
        try:
            with open(filepath) as f:
                emails = csv.reader(f)
                # There were A LOT duplicated emails.
                emails = set([email[0] for email in emails])

        except OSError:
            raise CommandError(f'{filepath} not found.')
        
        if Subscriber.objects.count() != 0:
            r = input(self.style.WARNING(
                'Existing records will be deleted. Continue? [Y/n]'
            ))
            if r.upper() == 'Y':
                print(
                    '{} records deleted.'
                    .format(Subscriber.objects.all().delete())
                )
            else:
                print(self.style.NOTICE('Aborted.'))
                return

        subscribers = []
        for email in emails:
            subscribers.append(Subscriber(email=email))
        subscribers = Subscriber.objects.bulk_create(subscribers)

        print(self.style.SUCCESS(
            'Successfully loaded previous subscribers, {} in total'
            .format(len(subscribers))
        ))