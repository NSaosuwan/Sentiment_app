# Generated by Django 4.0.2 on 2022-02-06 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Class', models.FloatField()),
                ('Detail', models.TextField()),
                ('Department', models.CharField(max_length=200)),
                ('Aspect', models.CharField(max_length=200)),
            ],
        ),
    ]
