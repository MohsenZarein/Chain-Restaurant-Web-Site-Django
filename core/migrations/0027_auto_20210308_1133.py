# Generated by Django 2.2.1 on 2021-03-08 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20210302_1813'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customerphoneno',
            unique_together={('customer', 'phone')},
        ),
        migrations.AlterUniqueTogether(
            name='personnelphoneno',
            unique_together={('personnel', 'phone')},
        ),
    ]
