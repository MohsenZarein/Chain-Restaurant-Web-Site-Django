# Generated by Django 2.2.1 on 2021-02-20 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_branch_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]