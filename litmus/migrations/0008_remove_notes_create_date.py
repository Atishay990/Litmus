# Generated by Django 3.0.4 on 2020-05-17 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('litmus', '0007_auto_20200517_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='create_date',
        ),
    ]
