# Generated by Django 2.2.8 on 2020-02-18 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_contactpage_seo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpage',
            name='google_ad_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]