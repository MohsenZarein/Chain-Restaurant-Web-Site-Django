# Generated by Django 2.2.1 on 2021-02-16 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_customerphoneno_personnelphoneno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branch_code', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('phone', models.CharField(max_length=50)),
                ('personnel_count', models.IntegerField(default=0)),
                ('province', models.CharField(max_length=225)),
                ('city', models.CharField(max_length=225)),
                ('street', models.CharField(max_length=225)),
                ('alley', models.CharField(max_length=225)),
            ],
        ),
    ]