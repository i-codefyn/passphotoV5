# Generated by Django 4.2.5 on 2024-02-28 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photomaker', '0004_croppedimage_alter_photomaker_file'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CroppedImage',
        ),
    ]
