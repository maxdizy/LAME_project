# Generated by Django 4.1.7 on 2023-07-12 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MADI', '0005_irfdata_alter_config_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='dart',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='config',
            name='file',
            field=models.FileField(default=False, upload_to=''),
        ),
        migrations.AlterField(
            model_name='config',
            name='mod',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='irfdata',
            name='ROED',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='irfdata',
            name='dart',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='irfdata',
            name='file',
            field=models.FileField(default=False, upload_to=''),
        ),
        migrations.AlterField(
            model_name='irfdata',
            name='mod',
            field=models.BooleanField(default=False),
        ),
    ]
