# Generated by Django 2.2.1 on 2021-02-21 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210221_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineorder',
            name='deliverer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Personnel'),
        ),
    ]