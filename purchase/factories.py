
from .models import Order,Receipt,ReceiptDetail,OrderDetail
from stock.models import Product,ProductCategory,Warehouse,Supplier
import pytz
from faker import Faker
import random
import factory


class ProductCategoryFactory(factory.django.DjangoModelFactory):
    reference = factory.Sequence(lambda n: 'cat00%d' % n) # factory.Iterator(["cat001", "cat002", "cat003"])
    name = factory.Sequence(lambda n: 'Category %d' % n) # factory.Iterator(["Category 1", "Category 2", "Category 3"])
    # reference = factory.Sequence(lambda n: 'cat %d' % n)
    # name = factory.Faker('company')

    class Meta:
        model = ProductCategory
        django_get_or_create = ('reference',)



class ProductFactory(factory.django.DjangoModelFactory):

    category = factory.SubFactory(ProductCategoryFactory)
    reference = factory.Sequence(lambda n: 'sku %d' % n)
    cost = factory.Faker(
        'pydecimal',
        left_digits=None,
        right_digits=None,
        positive=True,
        min_value=10,
        max_value=500
    )
    weight = factory.Faker(
        'pydecimal',
        left_digits=None,
        right_digits=None,
        positive=True,
        min_value=1,
        max_value=50
    )
    weight_unit = factory.LazyFunction(lambda: random.choice(['kg']))
    volume = factory.Faker(
        'pydecimal',
        left_digits=None,
        right_digits=None,
        positive=True,
        min_value=1,
        max_value=100
    )
    volume_unit = factory.LazyFunction(lambda: random.choice(['cm3']))

    product_type = factory.Iterator(['PV', 'AP', 'CS'])
    product_ray = factory.Iterator(['Food', 'Non Food'])
    product_universe = factory.Iterator(['Groupe', 'Non Groupe'])

    class Meta:
        model = Product
        django_get_or_create = ('reference',)



class WarehouseFactory(factory.django.DjangoModelFactory):
    # name = factory.Iterator(["Warehouse 1", "Warehouse 2", "Warehouse 3"])
    name = factory.Sequence(lambda n: 'Warehouse_%d' % n) # 'Name {0}'.format(n)
    lat = factory.Faker('coordinate', center=32.4581643, radius=2.5)
    lon = factory.Faker('coordinate', center=-5.884532, radius=2)
    address = factory.Faker('address')

    class Meta:
        model = Warehouse
        django_get_or_create = ('name',)

class OrderFactory(factory.django.DjangoModelFactory):
    reference = factory.Sequence(lambda n: 'order_%d' % n)
    ordered_at = factory.Faker(
        'past_datetime',
        start_date='-2y',
        tzinfo=pytz.utc
    )
    class Meta:
        model = Order
        django_get_or_create = ('reference',)

class ReceiptFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Receipt


class ReceiptDetailFactory(factory.django.DjangoModelFactory):


    unit_cost = factory.Faker(
        'pydecimal',
        left_digits=None,
        right_digits=None,
        positive=True,
        min_value=10,
        max_value=500
    )

    receipted_quantity = factory.Faker(
        'pyint',
        min_value=10,
        max_value=500
    )
    class Meta:
        model = ReceiptDetail

class SupplierFactory(factory.django.DjangoModelFactory):
    reference = factory.Sequence(lambda n: 'customer %d' % n)
    address = factory.Faker('address')

    class Meta:
        model = Supplier
        django_get_or_create = ('reference',)

class OrderDetailFactory(factory.django.DjangoModelFactory):

    ordered_quantity = factory.Faker(
        'pyint',
        min_value=10,
        max_value=500
    )

    unit_price = factory.Faker(
        'pydecimal',
        left_digits=None,
        right_digits=None,
        positive=True,
        min_value=10,
        max_value=500
    )


    class Meta:
        model = OrderDetail

    

    @factory.post_generation
    def create_orderdetail(self, create, how_many, **kwargs):
        at_least = 1 
        fake = Faker()
        random_date_this_year = fake.date_time_between(start_date='-2m', end_date='+2m')
        
        self.order = random.choice(orders)
        self.warehouse = random.choice(warehouses)
        self.product = random.choice(products)
        self.desired_at = random_date_this_year


        # if not create:
        #     return
       
        for n in range(how_many or at_least):
            # Generate random date

            # Generate warehouses
            random_date_this_year_receipt_at = Faker().date_time_between(start_date='-1y', end_date='+1y')
            random_date_this_year_expedit_at = Faker().date_time_between(start_date='-1y', end_date='+1y')

            ReceiptDetailFactory(
                product=self.product,
                order=self.order,
                order_detail=self,
                receipt_at = random_date_this_year_receipt_at,
                expedit_at = random_date_this_year_expedit_at,
                receipt = random.choice(receipts),
                warehouse = random.choice(warehouses),
                status = random.choice(status),
            )
                

warehouse_1 = WarehouseFactory.create(reference='War1')
warehouse_2 = WarehouseFactory.create(reference='War2')
warehouse_3 = WarehouseFactory.create(reference='War3')


warehouses=[warehouse_1,warehouse_2,warehouse_3]

# Generate cats

cat1 = ProductCategoryFactory.create(reference='cat15')
cat2 = ProductCategoryFactory.create(reference='cat16')
cat3 = ProductCategoryFactory.create(reference='cat17')


# Generate products
product_1 = ProductFactory.create(reference='product19',category=cat1)
product_2 = ProductFactory.create(reference='product20',category=cat2)
product_3 = ProductFactory.create(reference='product21',category=cat3)

products = [product_1,product_2,product_3]

status = ['A', 'Q', 'R','PD','SR']


# Generate suppliers
supplier_1 = SupplierFactory.create(
    reference='supplier19')
supplier_2 = SupplierFactory.create(
    reference='supplier2994')
supplier_3 = SupplierFactory.create(
    reference='supplier3994',)
suppliers = [supplier_1, supplier_2, supplier_3]

# Generate Orders


order_1 = OrderFactory(
    supplier = random.choice(suppliers),
)

order_2 = OrderFactory(

    supplier = random.choice(suppliers),
)
order_3 = OrderFactory(

    supplier = random.choice(suppliers),
)

order_4 = OrderFactory(

    supplier = random.choice(suppliers),
)

orders = [order_1,order_2,order_3,order_4]

receipt_1 = ReceiptFactory(
    supplier = random.choice(suppliers),
)

receipt_2 = ReceiptFactory(
    supplier = random.choice(suppliers),
)

receipt_3 = ReceiptFactory(
    supplier = random.choice(suppliers),
)

receipt_4 = ReceiptFactory(
    supplier = random.choice(suppliers),
)

receipts = [receipt_1,receipt_2,receipt_3,receipt_4]