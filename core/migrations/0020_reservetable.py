# Generated by Django 2.2.1 on 2021-02-27 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20210227_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Branch')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Customer')),
                ('personnel_as_customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Personnel')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Table')),
            ],
        ),
    ]
