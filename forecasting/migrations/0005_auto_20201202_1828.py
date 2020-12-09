# Generated by Django 3.0.2 on 2020-12-02 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forecasting', '0004_auto_20201202_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_versions', to=settings.AUTH_USER_MODEL),
        ),
    ]
