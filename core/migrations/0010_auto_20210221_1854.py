# Generated by Django 2.2.1 on 2021-02-21 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_onlineorder_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='alley',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='province',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='street',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]
