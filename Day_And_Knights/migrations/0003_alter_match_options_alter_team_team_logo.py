# Generated by Django 4.1.7 on 2023-03-25 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Day_And_Knights', '0002_remove_league_teams_team_league'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name_plural': 'matches'},
        ),
        migrations.AlterField(
            model_name='team',
            name='team_logo',
            field=models.ImageField(blank=True, null=True, upload_to='team_logos/'),
        ),
    ]
