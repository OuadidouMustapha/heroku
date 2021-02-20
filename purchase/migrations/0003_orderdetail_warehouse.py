# Generated by Django 3.0.2 on 2021-02-18 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_productcategory_monthly_capacity'),
        ('purchase', '0002_orderdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topic_content_type', to='stock.Warehouse'),
        ),
    ]
