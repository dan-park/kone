from django.db import models

# Create your models here.




class Biome(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Sample(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    biome = models.ForeignKey(Biome, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ContigToBlastResult(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    contig_name = models.CharField(max_length=30)
    subject = models.CharField(max_length=50)
    pident = models.FloatField()
    alignment_length = models.IntegerField()
    mismatch = models.IntegerField()
    gap_open = models.IntegerField()
    contig_start = models.IntegerField()
    contig_end = models.IntegerField()
    subject_start = models.IntegerField()
    subject_end = models.IntegerField()
    evalue = models.FloatField()
    bitsocre = models.FloatField()



class ContigToBlast2(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    contig_name = models.CharField(max_length=30)
    subject = models.CharField(max_length=50)
    pident = models.FloatField()
    alignment_length = models.IntegerField()
    mismatch = models.IntegerField()
    gap_open = models.IntegerField()
    contig_start = models.IntegerField()
    contig_end = models.IntegerField()
    subject_start = models.IntegerField()
    subject_end = models.IntegerField()
    evalue = models.FloatField()
    bitsocre = models.FloatField()
    contig_coverage = models.FloatField()


class SequenceIdToTaxon(models.Model):
    subject = models.CharField(max_length=50)
    taxon_id = models.IntegerField()

    class Meta:
        unique_together = ('subject', 'taxon_id')


class GiToTaxon(models.Model):
    gi = models.BigIntegerField()
    taxon = models.IntegerField()


class TaxonDB(models.Model):
    taxon_id = models.IntegerField()
    taxon_name = models.CharField(max_length=300)
    taxon_unique = models.CharField(max_length=100)
    taxon_name_class = models.CharField(max_length=30)


def get_raw_upload_path(instance, filename):
    sample_name = instance.sample.name
    file_name = filename
    return '{0}/{1}'.format(sample_name, file_name)
    #return self.sample.name + "/" + file_type
    #return '{0}/{1}'.format(str(Sample.objects.get(id=instance.sample_id).name), filename)


class RawFiles(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
    fastq_r1 = models.FileField(upload_to=get_raw_upload_path, blank=True, null=True)
    fastq_r2 = models.FileField(upload_to=get_raw_upload_path, blank=True, null=True)
    contigs = models.FileField(upload_to=get_raw_upload_path, blank=True, null=True)

    def __str__(self):
        return self.sample.name


class ARG(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)


class ARO(models.Model):
    aro = models.CharField(max_length=30)
    cvterm = models.IntegerField()
    model_sequence_id = models.IntegerField()
    model_id = models.IntegerField()
    model_name = models.CharField(max_length=100)
    aro_name = models.CharField(max_length=100)
    protein_acc = models.CharField(max_length=50)
    dna_acc = models.CharField(max_length=50)


class AROCategories(models.Model):
    protein_acc = models.CharField(max_length=50)
    dna_acc = models.CharField(max_length=50)
    amr_gene_family = models.CharField(max_length=100)
    amr_drug_class = models.CharField(max_length=100)
    amr_resistance_mechanism = models.CharField(max_length=100)


class AROGeneFamily(models.Model):
    protein_acc = models.CharField(max_length=50)
    dna_acc = models.CharField(max_length=50)
    amr_gene_family = models.CharField(max_length=100)


class ARODrugClass(models.Model):
    protein_acc = models.CharField(max_length=50)
    dna_acc = models.CharField(max_length=50)
    amr_drug_class = models.CharField(max_length=100)


class AROResistanceMechanism(models.Model):
    protein_acc = models.CharField(max_length=50)
    dna_acc = models.CharField(max_length=50)
    amr_resistance_mechanism = models.CharField(max_length=100)


class ProteinModel(models.Model):
    protein_acc = models.CharField(max_length=50)
    aro = models.CharField(max_length=30)
    protein_name = models.CharField(max_length=50)
    taxon_origin = models.CharField(max_length=100)
    length = models.IntegerField(null=True)
    sequence = models.TextField(null=True)


#class ARO_Protein(models.Model):
#    aro = models.CharField(max_length=30)
class SampleToContigToLocus(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    contig_name = models.CharField(max_length=30)
    locus_name = models.CharField(max_length=30)


# Diamond Alignment Result
class ContigLocusToARO(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    locus_name = models.CharField(max_length=30)
    aro = models.CharField(max_length=30)
    pident = models.FloatField()
    aln_length = models.IntegerField()
    num_mismatch = models.IntegerField()
    gap_open = models.IntegerField()
    qstart = models.IntegerField()
    qend = models.IntegerField()
    aro_start = models.IntegerField()
    aro_end = models.IntegerField()
    evalue = models.FloatField()
    bitscore = models.FloatField()


# Diamond Alignment Result
class ContigToARO(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    contig_name = models.CharField(max_length=30)
    aro = models.CharField(max_length=30)
    pident = models.FloatField()
    aln_length = models.IntegerField()
    num_mismatch = models.IntegerField()
    gap_open = models.IntegerField()
    qstart = models.IntegerField()
    qend = models.IntegerField()
    aro_start = models.IntegerField()
    aro_end = models.IntegerField()
    evalue = models.FloatField()
    bitscore = models.FloatField()


#class SampleToGenePrediction(models.Model):
#    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
#    locus_name = models.CharField(max_length=30)
#    ftype = models.CharField(max_length=30)
#    length = models.IntegerField()
#    gene = models.CharField(max_length=30)
#    ec_number = models.CharField(max_length=30)
#    cog_product = models.CharField(max_length=100)


class SampleToGeneProteinSequence(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    locus_name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    protein_seq = models.TextField()



class SampleToContigs(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    contig_name = models.CharField(max_length=30)
    contig_header = models.CharField(max_length=100)
    contig_length = models.IntegerField()
    contig_seq = models.TextField()

    class Meta:
        unique_together = ('sample', 'contig_name')

    def __str__(self):
        return '{0}/{1}'.format(self.sample.name, self.contig_name)




#class ContigToLocusTag(models.Model):
#    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
#    contig_name = models.CharField(max_length=30)
#    locus_tag = models.CharField(max_length=30)


#class LocusTagToARG(models.Model):
#    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
#    contig_name = models.CharField(max_length=30)
#    locus_tag = models.CharField(max_length=30)
#    arg_name = models.CharField(max_length=30)