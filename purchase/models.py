from django.db import models
from stock.models import Supplier, Product, Warehouse

# Create your models here.


class CommonMeta(models.Model):
    CREATED = 'Created'
    ACTIVE = 'Active'
    ARCHIVED = 'Archived'
    STATUS = (
        (CREATED, 'Created'),
        (ACTIVE, 'Active'),
        (ARCHIVED, 'Archived'),
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=CREATED,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Order(CommonMeta):
    reference = models.CharField(unique=True, max_length=200)
    ordered_at = models.DateField(blank=True, null=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.reference}'


class OrderDetail(CommonMeta):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, blank=True, null=True, related_name='purchase_orderdetail_set')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True, related_name='purchase_orderdetail_set')
    ordered_quantity = models.IntegerField(blank=True, null=True)
    unit_price = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    desired_at = models.DateTimeField(blank=True, null=True)


class Receipt(CommonMeta):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True)
    reference = models.CharField(max_length=200, blank=True, null=True)
    receipt_at = models.DateField(blank=True, null=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, blank=True, null=True)


class ReceiptDetail(CommonMeta):
    A = 'A'
    Q = 'Q'
    R = 'R'
    RD = 'PD'
    SR = 'SR'
    STATUS = (
        (A, 'Accepted'),
        (Q, 'Pending Quality Control'),
        (R, 'Rejected'),
        (RD, 'Product To Be Destroyed'),
        (SR, 'Supplier Return'),
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True)
    order_detail = models.ForeignKey(
        OrderDetail, on_delete=models.CASCADE, blank=True, null=True)
    receipt = models.ForeignKey(
        Receipt, on_delete=models.CASCADE, blank=True, null=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True)
    receipted_quantity = models.IntegerField(blank=True, null=True)
    unit_cost = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=A,
        null=True, blank=True
    )
    receipt_at = models.DateTimeField(auto_now_add=True)
