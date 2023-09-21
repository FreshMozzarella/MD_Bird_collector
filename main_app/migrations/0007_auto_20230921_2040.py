# Generated by Django 3.2.12 on 2023-09-21 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20230921_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bird',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='bird_audio/'),
        ),
        migrations.AlterField(
            model_name='bird',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='bird_images/'),
        ),
    ]
