# Generated by Django 2.2.1 on 2021-03-02 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Table'),
        ),
    ]