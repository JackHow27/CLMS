# Generated by Django 4.1.7 on 2023-04-23 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Day_And_Knights', '0002_alter_team_captain_alter_team_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='result',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
