import csv
from django.core.management.base import BaseCommand
from sample_uk_meds.models import Manufacturer, Formula, Medicine

class Command(BaseCommand):
    help = 'Import medicines from BNF_Codes.csv'

    def handle(self, *args, **kwargs):
        with open('BNF_Codes.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                manufacturer, _ = Manufacturer.objects.get_or_create(name=row['manufacturer_name'].strip())
                formula, _ = Formula.objects.get_or_create(name=row['formula'].strip())
                Medicine.objects.create(
                    bnf_code=row['bnf_code'].strip(),
                    formula=formula,
                    dose=row['dose'].strip(),
                    manufacturer=manufacturer,
                    price=row['price'].strip(),
                    brand_name=row['brand_name'].strip(),
                    generic_available=row['generic_available'].strip().lower() == 'true'
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Imported {count} medicines.'))
