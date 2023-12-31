# Generated by Django 4.2.3 on 2023-09-14 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarms', '0003_alter_detail_alarm_code_delete_alarmresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.IntegerField()),
                ('account_name', models.CharField(max_length=255)),
                ('user_name', models.CharField(max_length=255)),
                ('license_number', models.CharField(blank=True, max_length=255, null=True)),
                ('vin', models.CharField(blank=True, max_length=255, null=True)),
                ('car_owner', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='VehicleStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('imei', models.CharField(max_length=20)),
                ('lat', models.CharField(blank=True, max_length=20, null=True)),
                ('lng', models.CharField(blank=True, max_length=20, null=True)),
                ('time', models.IntegerField()),
                ('position_type', models.CharField(blank=True, max_length=20, null=True)),
                ('speed', models.IntegerField(blank=True, null=True)),
                ('course', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(max_length=255)),
                ('acc_status', models.BooleanField()),
                ('end_time', models.IntegerField()),
                ('platform_end_time', models.IntegerField()),
                ('activate_time', models.IntegerField()),
                ('status_time_desc', models.CharField(max_length=255)),
                ('signal_time', models.IntegerField()),
                ('gps_time', models.IntegerField()),
                ('is_wireless', models.IntegerField()),
                ('sim', models.CharField(max_length=255)),
                ('ext_voltage', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Estado del vehículo',
                'verbose_name_plural': 'Estados del vehículo',
            },
        ),
        migrations.AlterModelOptions(
            name='detail',
            options={'verbose_name': 'Código de alarma', 'verbose_name_plural': 'Alarma'},
        ),
    ]
