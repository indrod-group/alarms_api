# Generated by Django 4.2.3 on 2023-09-14 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alarms', '0004_user_vehiclestatus_alter_detail_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclestatus',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_statuses', to='alarms.user'),
            preserve_default=False,
        ),
    ]