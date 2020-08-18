# Generated by Django 3.0.2 on 2020-08-18 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockForecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Active', 'Active'), ('Archived', 'Archived')], default='Created', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('forecast_date', models.DateField(blank=True, null=True)),
                ('forecast_version', models.DateField(auto_now_add=True)),
                ('forecasted_quantity', models.IntegerField(blank=True, null=True)),
                ('circuit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Circuit')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Customer')),
                ('stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Stock')),
            ],
        ),
        migrations.AddConstraint(
            model_name='stockforecast',
            constraint=models.UniqueConstraint(fields=('stock', 'forecast_date', 'circuit', 'forecast_version'), name='stockforecast_stock_sp_fd_uniq'),
        ),
    ]
