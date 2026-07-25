from django.core.management.base import BaseCommand

from locations.data import PROVINCES, DISTRICTS
from locations.models import Province, District


class Command(BaseCommand):
    help = "Seed Province and District data"

    def handle(self, *args, **kwargs):

        # Seed Provinces
        for province_name in PROVINCES:

            province, created = Province.objects.get_or_create(
                name=province_name
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created Province: {province.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Province already exists: {province.name}")
                )

        # Seed Districts
        for province_name, district_list in DISTRICTS.items():

            province = Province.objects.get(
                name=province_name
            )

            for district_name in district_list:

                district, created = District.objects.get_or_create(
                    name=district_name,
                    province=province
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created District: {district.name}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"District already exists: {district.name}"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Location seeding completed successfully!"
            )
        )