import csv
import os
from django.core.management.base import BaseCommand
from iGEMResearcher.models import Team  # 適切なパスに修正してください

class Command(BaseCommand):
    help = 'Imports teams from CSV files in the specified directory into the database'

    def add_arguments(self, parser):
        # ディレクトリパスを引数として追加
        parser.add_argument('csv_dir', type=str, help='The directory of CSV files')

    def handle(self, *args, **options):
        csv_dir = options['csv_dir']
        for filename in os.listdir(csv_dir):
            if filename.endswith('.csv'):
                file_path = os.path.join(csv_dir, filename)
                self.stdout.write(f'Importing teams from {file_path}')
                with open(file_path, mode='r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        Team.objects.create(
                            team=row['team'],
                            wiki=row['wiki'],
                            region=row['region'],
                            country=row['country'],
                            track=row['track'],
                            kind=row['kind'],
                            section=row['section'],
                            year=int(row['year']),
                            description=''  # 初期値として空の文字列を設定
                        )
                self.stdout.write(self.style.SUCCESS(f'Successfully imported teams from {file_path}'))
