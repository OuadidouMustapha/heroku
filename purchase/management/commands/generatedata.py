from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from purchase.factories import OrderDetailFactory
from purchase.models import (OrderDetail, Receipt,ReceiptDetail, Order)

'''
Command 'generatedemodata' parameters file
'''

class Command(BaseCommand):
    help = "Populate the app with sample data. Generates Order and OrderDetail."


    def _load_fixtures(self):
        # ProductCategoryFactory.create_batch(size=10)
        # WarehouseFactory.create_batch(size=3)
        OrderDetailFactory.create_batch(size=40) 

    def _clean_db(self):
        for model in [OrderDetail, Receipt,ReceiptDetail, Order]:
            model.objects.all().delete()

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                if options['clean']:
                    self._clean_db()
                self._load_fixtures()

        except Exception as e:
            raise CommandError(
                f"{e}\n\nTransaction was not committed due to the above exception.")


    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            help='Wipe existing data from the database before loading fixtures.',
            action='store_true',
            default=False,
        )



