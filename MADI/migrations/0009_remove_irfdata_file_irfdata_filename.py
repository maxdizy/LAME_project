# Generated by Django 4.1.7 on 2023-07-12 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MADI', '0008_alter_config_file_alter_config_mod_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='irfdata',
            name='file',
        ),
        migrations.AddField(
            model_name='irfdata',
            name='fileName',
            field=models.CharField(default='', max_length=200),
        ),
    ]
