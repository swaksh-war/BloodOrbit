# Generated by Django 5.0.2 on 2025-02-08 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('long_term_disease', models.CharField(blank=True, max_length=1000, null=True)),
                ('blood_group', models.CharField(max_length=3)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('contact_number', models.BigIntegerField()),
                ('last_time_donated', models.DateTimeField(auto_now_add=True)),
                ('registered_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
