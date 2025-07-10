from django.core.management.base import BaseCommand
from sample_uk_meds.models import Medicine
import urllib.parse

class Command(BaseCommand):
    help = 'Update emc_leaflet_url for all medicines using only medicine name.'

    def handle(self, *args, **options):
        updated = 0
        for med in Medicine.objects.all():
            # Use only the medicine name for the EMC search query
            query = f"{med.medicine_name}"
            url = f"https://www.medicines.org.uk/emc/search?q={urllib.parse.quote_plus(query)}"
            if med.emc_leaflet_url != url:
                med.emc_leaflet_url = url
                med.save(update_fields=["emc_leaflet_url"])
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"Updated EMC link for: {med.medicine_name}"))
        self.stdout.write(self.style.SUCCESS(f"Done. Updated EMC links for {updated} medicines."))
