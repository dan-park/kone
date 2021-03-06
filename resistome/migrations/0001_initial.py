# Generated by Django 2.1.2 on 2018-11-14 05:40

from django.db import migrations, models
import django.db.models.deletion
import resistome.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ARG',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ARO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aro', models.CharField(max_length=30)),
                ('cvterm', models.IntegerField()),
                ('model_sequence_id', models.IntegerField()),
                ('model_id', models.IntegerField()),
                ('model_name', models.CharField(max_length=100)),
                ('aro_name', models.CharField(max_length=100)),
                ('protein_acc', models.CharField(max_length=50)),
                ('dna_acc', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Biome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RawFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fastq_r1', models.FileField(blank=True, null=True, upload_to=resistome.models.get_raw_upload_path)),
                ('fastq_r2', models.FileField(blank=True, null=True, upload_to=resistome.models.get_raw_upload_path)),
                ('contigs', models.FileField(blank=True, null=True, upload_to=resistome.models.get_raw_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('biome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resistome.Biome')),
            ],
        ),
        migrations.CreateModel(
            name='SampleToContigs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contig_name', models.CharField(max_length=30)),
                ('contig_header', models.CharField(max_length=100)),
                ('contig_length', models.IntegerField()),
                ('contig_seq', models.TextField()),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resistome.Sample')),
            ],
        ),
        migrations.AddField(
            model_name='rawfiles',
            name='sample',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='resistome.Sample'),
        ),
        migrations.AlterUniqueTogether(
            name='sampletocontigs',
            unique_together={('sample', 'contig_name')},
        ),
    ]
