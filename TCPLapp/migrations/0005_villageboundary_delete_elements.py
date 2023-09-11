# Generated by Django 4.2.4 on 2023-09-06 05:39

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TCPLapp", "0004_villagetalukadata"),
    ]

    operations = [
        migrations.CreateModel(
            name="VillageBoundary",
            fields=[
                ("fid", models.BigIntegerField(primary_key=True, serialize=False)),
                ("geom", django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                (
                    "objectid",
                    models.BigIntegerField(blank=True, db_column="OBJECTID", null=True),
                ),
                (
                    "taluka",
                    models.CharField(
                        blank=True, db_column="Taluka", max_length=50, null=True
                    ),
                ),
                (
                    "area_in_ha",
                    models.FloatField(blank=True, db_column="Area_In_Ha", null=True),
                ),
                (
                    "village_name_census",
                    models.CharField(
                        blank=True,
                        db_column="Village_Name_Census",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "village_name_revenue",
                    models.CharField(
                        blank=True,
                        db_column="Village_Name_Revenue",
                        max_length=255,
                        null=True,
                    ),
                ),
                ("temp", models.IntegerField(blank=True, db_column="Temp", null=True)),
                (
                    "shape_length",
                    models.FloatField(blank=True, db_column="Shape_Length", null=True),
                ),
                (
                    "shape_area",
                    models.FloatField(blank=True, db_column="Shape_Area", null=True),
                ),
            ],
            options={"db_table": "Village_Boundary", "managed": False,},
        ),
        migrations.DeleteModel(name="elements",),
    ]
