import csv
from django.core.management.base import BaseCommand
from sample_uk_meds.models import Medicine

class Command(BaseCommand):
    help = 'Import medicines from UK_Medicines_Data.csv'

    def handle(self, *args, **kwargs):
        with open('UK_Medicines_Data.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            skipped = 0
            for row in reader:
                price_str = row['price'].replace('£', '').strip()
                try:
                    price = float(price_str)
                except ValueError:
                    price = 0.0
                rating = float(row.get('rating', row.get('rating (Demo only)', 0)))
                exists = Medicine.objects.filter(
                    medicine_name=row['medicine_name'],
                    formula=row['formula'],
                    dose=row['dose'],
                    manufacturer=row['manufacturer'],
                ).exists()
                if not exists:
                    Medicine.objects.create(
                        medicine_name=row['medicine_name'],
                        formula=row['formula'],
                        dose=row['dose'],
                        manufacturer=row['manufacturer'],
                        price=price,
                        rating=rating,
                    )
                    count += 1
                else:
                    skipped += 1
            self.stdout.write(self.style.SUCCESS(f'Imported {count} medicines. Skipped {skipped} duplicates.'))
