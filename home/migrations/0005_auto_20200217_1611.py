# Generated by Django 2.2.8 on 2020-02-17 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20200217_1545'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepage',
            old_name='body',
            new_name='my_stream',
        ),
    ]