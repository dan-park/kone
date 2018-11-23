# Generated by Django 2.1.2 on 2018-11-22 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resistome', '0012_gitotaxon'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxonDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxon_id', models.IntegerField()),
                ('taxon_name', models.CharField(max_length=100)),
                ('taxon_unique', models.CharField(max_length=100)),
                ('taxon_name_class', models.CharField(max_length=30)),
            ],
        ),
    ]