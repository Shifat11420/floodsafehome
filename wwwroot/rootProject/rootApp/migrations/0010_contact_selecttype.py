# Generated by Django 3.2.5 on 2021-08-30 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rootApp', '0009_alter_contact_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='selecttype',
            field=models.CharField(default='SOME STRING', max_length=100),
        ),
    ]