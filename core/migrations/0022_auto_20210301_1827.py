# Generated by Django 2.2.1 on 2021-03-01 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20210301_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
