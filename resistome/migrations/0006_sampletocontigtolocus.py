# Generated by Django 2.1.2 on 2018-11-14 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resistome', '0005_auto_20181114_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleToContigToLocus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contig_name', models.CharField(max_length=30)),
                ('locus_name', models.CharField(max_length=30)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resistome.Sample')),
            ],
        ),
    ]
