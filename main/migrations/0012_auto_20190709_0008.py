# Generated by Django 2.2.2 on 2019-07-08 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_patient_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
