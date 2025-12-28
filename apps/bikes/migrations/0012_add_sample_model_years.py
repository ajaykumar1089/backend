# Generated migration to add sample model year data

from django.db import migrations

def add_sample_model_years(apps, schema_editor):
    BikeModelYear = apps.get_model('bikes', 'BikeModelYear')
    
    # Add sample model years
    years = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015]
    
    for year in years:
        BikeModelYear.objects.get_or_create(year=year)

def remove_sample_model_years(apps, schema_editor):
    BikeModelYear = apps.get_model('bikes', 'BikeModelYear')
    BikeModelYear.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('bikes', '0011_rename_model_year_field'),
    ]

    operations = [
        migrations.RunPython(add_sample_model_years, remove_sample_model_years),
    ]