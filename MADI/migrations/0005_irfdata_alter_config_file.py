# Generated by Django 4.1.7 on 2023-07-12 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MADI', '0004_alter_config_dart_alter_config_mod'),
    ]

    operations = [
        migrations.CreateModel(
            name='IRFdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CN', models.CharField(max_length=200)),
                ('tail', models.CharField(max_length=200)),
                ('IRFTitle', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('affected', models.CharField(max_length=200)),
                ('IRFNo', models.CharField(max_length=200)),
                ('ROED', models.BooleanField()),
                ('dart', models.BooleanField()),
                ('mod', models.BooleanField()),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='config',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
