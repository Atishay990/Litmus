# Generated by Django 3.0.4 on 2020-05-17 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('litmus', '0009_notes_create_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notes',
            old_name='create_date',
            new_name='create_time',
        ),
    ]
