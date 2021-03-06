# Generated by Django 3.0 on 2019-12-16 21:35

from django.db import migrations
import csv
from search.models import School, PrivateInstitutionData, Address, ContactData


def load_data_private_lo_adult(apps, schema):
    with open('csvs/niepubliczne_lo_dorosli.csv', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_number = 0
        for row in csv_reader:
            if row_number == 0:
                row_number += 1
            else:
                row_number += 1
                print(f'row {row_number} inserted')

                school = School()
                address = Address()
                address.district = row[0]

                # some schools have different locations written in brackets with their name
                school.school_name = row[1].split('(')[0]
                address.street = row[2]
                address.building_nr = row[3]
                address.postcode = row[4].strip()
                address.city = row[5]
                data = PrivateInstitutionData()
                data.registration_nr = row[6]
                school.school_type = 'liceum ogólnokształcące'
                school.school_type_generalised = 'szkoła ponadpodstawowa'
                school.student_type = 'dorosli'
                school.address = address
                school.private_institution_data = data
                school.is_public = False
                data.save()
                address.save()
                school.save()

class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_insert_niepubliczne_lo_mlodziez'),

    ]

    operations = [
        migrations.RunPython(load_data_private_lo_adult)
    ]
