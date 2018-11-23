
# Diamond Alignment Result
#class ContigLocusToARO(models.Model):
#    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
#    locus_name = models.CharField(max_length=30)
#    aro = models.CharField(max_length=30)
#    pident = models.FloatField()
#    aln_length = models.IntegerField()
#    num_mismatch = models.IntegerField()
#    gap_open = models.IntegerField()
#    qstart = models.IntegerField()
#    qend = models.IntegerField()
#    aro_start = models.IntegerField()
#    aro_end = models.IntegerField()
#    evalue = models.FloatField()
#    bitscore = models.FloatField()

import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys
import getopt
import csv


if __name__ == "__main__":

    sample_name = ''
    prokka_diamond = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:i:", ["sample=", "c2p="])
    except getopt.GetoptError:
        print('z05.insert_contigs_prokka.py -s <samplename> -i <prokka_card_diamond.tsv>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('z05.insert_contigs_prokka.py -s <samplename> -i <prokka_card_diamond.tsv>')
            sys.exit(1)
        elif opt in ("-s", "--sample"):
            sample_name = arg
        elif opt in ("-i", "--prokka2card"):
            prokka_diamond = arg

    print(sample_name)
    print(prokka_diamond)

    conn = pg.connect("host=localhost dbname=onehealth user=onehealth password=oh123")
    conn.autocommit = True
    cur = conn.cursor()

    folder = Path(prokka_diamond)
    table_name = "resistome_contiglocustoaro"

    sample_id = "'"+sample_name+"'"
    with open(folder) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            locus_name = "'"+row[0]+"'"
            aro_infos = row[1].split("|")
            aro = "'" + aro_infos[2] + "'"
            pident = row[2]
            aln_length = row[3]
            num_mismatch = row[4]
            gap_open = row[5]
            qstart = row[6]
            qend = row[7]
            aro_start = row[8]
            aro_end = row[9]
            evalue = row[10]
            bitscore = row[11]

            sql = "insert into " + table_name + ' (locus_name, aro, pident, aln_length, num_mismatch, gap_open, qstart, qend, aro_start, aro_end, evalue, bitscore, sample_id) values({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12})'.format(locus_name, aro, pident, aln_length, num_mismatch, gap_open, qstart, qend, aro_start, aro_end, evalue, bitscore, sample_id)
            print(sql)
            cur.execute(sql)

cur.close()
conn.close()
