# Generated by Django 3.2.5 on 2021-08-30 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rootApp', '0008_contact_detailmethodse2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=122),
        ),
    ]
