# Generated by Django 2.0.1 on 2018-01-04 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180104_1620'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ip_or_api',
            old_name='add_way_id',
            new_name='add_way',
        ),
        migrations.RenameField(
            model_name='ip_or_api',
            old_name='server_id',
            new_name='server',
        ),
    ]
