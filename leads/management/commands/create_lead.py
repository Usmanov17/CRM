from django.core.management.base import BaseCommand
from leads.models import Lead, Userprofile
from csv import DictReader

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)
        parser.add_argument('organizer_email', type=str)
     
    def handle(self, *args, **options):
        file_name=options['file_name']
        organizer_email=options['organizer_email']

        organisation=Userprofile.objects.get(user__email=organizer_email)

        with open(file_name, 'r') as red_obj:
            csv_reader=DictReader(red_obj)
            for row in csv_reader:
                first_name=row['first_name']
                last_name=row['last_name']
                age=row['age']
                email=row['email']

                Lead.objects.create(
                    organisation=organisation,
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    email=email,
                )

