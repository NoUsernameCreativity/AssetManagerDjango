# necessary imports
import csv
from django.core.management import BaseCommand, CommandError
from DjangoApp1.models import asset, teacher

# setting up command line interface
class Command(BaseCommand):

    # help message if --h typed into CLI. Built in var.
    help = "To add a CSV type --path, help --h. Use --import 'teacher' to import a teacher (asset is default)."

    def add_arguments(self, parser):
        # add arguments to command line interface
        # path to CSV file to be imported
        parser.add_argument('--path', type=str)
        parser.add_argument('--import', type=str)

    def handle(self, *args, **kwargs):
        # *args: arguments. Allows for a variable number of arguments.
        # **kwargs: keyword arguments. Same as arguments but instead of being passed as values they are passed as keywords
        # eg. path=... is a keyword argument
        path = kwargs['path'] # grab our argument
        # open the CSV file and read, to add the asset
        with open(path, 'rt', encoding='utf-8-sig') as file:
            reader = csv.reader(file, dialect='excel')
            # read first row to get titles
            for row in reader: # add each value to db
                if kwargs['import'] == 'teacher':
                    if len(row) != 2:
                        raise CommandError("Number of columns doesn't match 'name, area'. Did you mean to import an asset?")
                    teacher.objects.create(Name = row[0], Area=row[1])
                else:
                    if len(row) != 4:
                        raise CommandError("Number of columns doesn't match 'name, location, lastupdated, value'. Did you mean to import a teacher?")
                    asset.objects.create(Name = row[0], Location=row[1], Value=row[2], LastUpdated=row[3])

