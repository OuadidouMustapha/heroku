# Generated by Django 3.0.2 on 2020-12-01 11:34

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circuit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('reference', models.CharField(max_length=200, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Circuit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField(blank=True)),
                ('circuit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Circuit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference', models.CharField(blank=True, max_length=200, null=True)),
                ('delivered_at', models.DateField(blank=True, null=True)),
                ('delivered_quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True)),
                ('total_amount', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True)),
                ('weight_unit', models.TextField(blank=True)),
                ('volume', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True)),
                ('volume_unit', models.TextField(blank=True)),
                ('package_size', models.IntegerField(blank=True, null=True)),
                ('pallet_size', models.IntegerField(blank=True, null=True)),
                ('product_type', models.CharField(blank=True, max_length=20, null=True)),
                ('product_ray', models.CharField(blank=True, max_length=20, null=True)),
                ('product_universe', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'ordering': ['reference'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference', models.CharField(max_length=200, unique=True)),
                ('supplied_at', models.DateField(blank=True, null=True)),
                ('total_amount', models.IntegerField(blank=True, null=True)),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('available_trucks', models.IntegerField(blank=True, null=True)),
                ('reception_capacity', models.IntegerField(blank=True, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lon', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupplyDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unit_price', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Product')),
                ('supply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Supply')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StockPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('safety_stock', models.IntegerField(blank=True, null=True)),
                ('delivery_time', models.IntegerField(blank=True, null=True)),
                ('order_point', models.IntegerField(blank=True, null=True)),
                ('target_stock', models.IntegerField(blank=True, null=True)),
                ('stock', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stock.Stock')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StockControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('inventory_date', models.DateField(blank=True, null=True)),
                ('product_quantity', models.IntegerField(blank=True, null=True)),
                ('stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Stock')),
            ],
        ),
        migrations.AddField(
            model_name='stock',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Warehouse'),
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('min_dio', models.IntegerField(blank=True, null=True, verbose_name='Min DIO')),
                ('max_dio', models.IntegerField(blank=True, null=True, verbose_name='Max DIO')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='stock.ProductCategory')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
            managers=[
                ('tree', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.ProductCategory'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference', models.CharField(blank=True, max_length=200, null=True)),
                ('ordered_quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True)),
                ('unit_price', models.IntegerField(blank=True, null=True)),
                ('ordered_at', models.DateField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.ProductCategory')),
                ('circuit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Circuit')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Customer')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Product')),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Warehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference', models.CharField(max_length=200, unique=True)),
                ('invoicing_date', models.DateField(blank=True, null=True)),
                ('total_amount', models.IntegerField(blank=True, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Customer')),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Delivery')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeliveryDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unit_price', models.IntegerField(blank=True, null=True)),
                ('delivered_quantity', models.IntegerField(blank=True, null=True)),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Delivery')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Stock')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='delivery',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.ProductCategory'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='circuit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Circuit'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Customer'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Order'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Product'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Warehouse'),
        ),
        migrations.AddConstraint(
            model_name='stockcontrol',
            constraint=models.UniqueConstraint(fields=('stock', 'inventory_date'), name='stockcontrol_stock_sp_id_uniq'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['reference'], name='stock_produ_referen_908b13_idx'),
        ),
    ]
