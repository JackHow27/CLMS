# Generated by Django 4.1.7 on 2023-03-26 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('boards_per_match', models.IntegerField(default=6)),
                ('active', models.BooleanField(default=False)),
                ('day_to_play', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Wednesday', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('ecf_code', models.CharField(max_length=200)),
                ('username', models.CharField(default='a7f2c7e1f7a54b01897341683ec53d54', max_length=150, unique=True)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=200)),
                ('team_logo', models.ImageField(blank=True, null=True, upload_to='team_logos/')),
                ('description', models.TextField()),
                ('home_field', models.CharField(max_length=50)),
                ('home_address', models.CharField(max_length=100)),
                ('rank', models.IntegerField(default=0)),
                ('League', models.ManyToManyField(related_name='teams', to='Day_And_Knights.league')),
                ('captain', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Day_And_Knights.player')),
                ('players', models.ManyToManyField(related_name='teams', to='Day_And_Knights.player')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('result', models.CharField(blank=True, max_length=20)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_matches', to='Day_And_Knights.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_matches', to='Day_And_Knights.team')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='Day_And_Knights.league')),
            ],
            options={
                'verbose_name_plural': 'matches',
            },
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_number', models.IntegerField()),
                ('result', models.CharField(blank=True, choices=[('1-0', '1-0'), ('0-1', '0-1'), ('1/2-1/2', '1/2-1/2'), ('*', '*')], max_length=10)),
                ('result_reason', models.TextField(blank=True)),
                ('black_player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='black_boards', to='Day_And_Knights.player')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to='Day_And_Knights.match')),
                ('white_player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='white_boards', to='Day_And_Knights.player')),
            ],
        ),
    ]
