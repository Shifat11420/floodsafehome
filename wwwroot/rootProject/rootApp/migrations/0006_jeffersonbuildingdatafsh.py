# Generated by Django 3.2.5 on 2021-07-07 06:24

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rootApp', '0005_dataall'),
    ]

    operations = [
        migrations.CreateModel(
            name='JeffersonbuildingdataFSH',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FID_1', models.BigIntegerField()),
                ('BLDG_ID', models.CharField(max_length=10, null=True)),
                ('HEIGHT', models.FloatField()),
                ('FOOTPRINT', models.FloatField()),
                ('address', models.CharField(max_length=100, null=True)),
                ('street', models.CharField(max_length=200, null=True)),
                ('no_floors', models.FloatField()),
                ('DATA_YEAR', models.CharField(max_length=10, null=True)),
                ('SFT', models.FloatField()),
                ('Area_SqMet', models.FloatField()),
                ('FloodDepth', models.FloatField()),
                ('FloodDep_1', models.FloatField()),
                ('FloodDep_2', models.FloatField()),
                ('FloodDep_3', models.FloatField()),
                ('ElevationU', models.FloatField()),
                ('Elevation', models.FloatField()),
                ('Elevatio_1', models.FloatField()),
                ('FID_2', models.BigIntegerField()),
                ('Source', models.CharField(max_length=50, null=True)),
                ('u_intercept', models.FloatField()),
                ('a_slope', models.FloatField()),
                ('Latitude', models.FloatField()),
                ('Longitude', models.FloatField()),
                ('FloodZone', models.CharField(max_length=100, null=True)),
                ('Parish', models.CharField(max_length=50, null=True)),
                ('mpoint', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
        ),
    ]
