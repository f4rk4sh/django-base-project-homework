# Generated by Django 3.2.8 on 2021-11-25 18:16

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdb_id', models.CharField(max_length=255, null=True, unique=True, verbose_name='imdb id')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('title_type', models.CharField(choices=[('short', 'Short'), ('movie', 'Movie')], default='short', max_length=80, verbose_name='Type of a title')),
                ('is_adult', models.BooleanField(default=False, verbose_name='Adult rated')),
                ('year', models.DateField(null=True, verbose_name='Release year')),
                ('genres', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default=list, max_length=80, verbose_name='Genres'), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdb_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='nconst')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('birth_year', models.DateField(blank=True, null=True, verbose_name='Birth date')),
                ('death_year', models.DateField(null=True, verbose_name='Death date')),
            ],
        ),
        migrations.CreateModel(
            name='PersonMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='ordering')),
                ('category', models.CharField(blank=True, max_length=100, null=True, verbose_name='Category')),
                ('job', models.CharField(blank=True, max_length=100, null=True, verbose_name='Job')),
                ('characters', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, verbose_name='Characters'), blank=True, null=True, size=None)),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='movies.movie')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='movies.person')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]