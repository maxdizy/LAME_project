# Generated by Django 4.1.7 on 2023-07-10 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MADI', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caseNo', models.CharField(max_length=200)),
                ('ERFpath', models.CharField(max_length=200)),
                ('dart', models.CharField(max_length=200)),
                ('mod', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='MADI/IRFs')),
            ],
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
