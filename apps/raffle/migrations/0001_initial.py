# Generated by Django 3.0.7 on 2020-06-12 18:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, unique=True, verbose_name='code')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('perday', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(86399)], verbose_name='perday')),
            ],
            options={
                'verbose_name': 'prize',
                'verbose_name_plural': 'prizes',
            },
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5, unique=True, verbose_name='code')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('start', models.DateField(verbose_name='start')),
                ('end', models.DateField(verbose_name='end')),
                ('win_at', models.DateTimeField(verbose_name='win at')),
                ('prize', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contests', to='raffle.Prize', verbose_name='prize')),
            ],
            options={
                'verbose_name': 'contest',
                'verbose_name_plural': 'contests',
            },
        ),
    ]
