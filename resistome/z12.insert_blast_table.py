import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys
import getopt
import csv


if __name__ == "__main__":

    sample_name = ''
    contig_to_blast = ''
    q_coverage_ratio_thr = 90

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:i:", ["sample=", "c2b="])
    except getopt.GetoptError:
        print('z09.insert_contigs_to_blast.py -s <samplename> -i <contigs_blast.tsv>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('z09.insert_contigs_to_blast.py -s <samplename> -i <contigs_blast.tsv>')
            sys.exit(1)
        elif opt in ("-s", "--sample"):
            sample_name = arg
        elif opt in ("-i", "--contig2blast"):
            contig_to_blast = arg

    print(sample_name)
    print(contig_to_blast)

    conn = pg.connect("host=localhost dbname=onehealth user=onehealth password=oh123")
    conn.autocommit = True
    cur = conn.cursor()

    folder = Path(contig_to_blast)
    table_name = "resistome_contigtoblast2"
    taxon_table = "resistome_sequenceidtotaxon"

    sample_id = "'"+sample_name+"'"
    with open(folder) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")

        for row in csv_reader:

            if not row[0].startswith("#"):
                print(row)
                contig_name = "'"+row[0]+"'"
                subject = "'"+row[1]+"'"
                pident = float(row[2])
                alignment_length = int(row[3])
                mismatch = int(row[4])
                gap_open = int(row[5])
                q_start = int(row[6])
                q_end = int(row[7])
                s_start = int(row[8])
                s_end = int(row[9])
                evalue = float(row[10])
                bitscore = float(row[11])
                q_coverage = float(row[12])
                taxonIds = row[13].split(";")

                if q_coverage >= q_coverage_ratio_thr:
                    sql = "insert into " + table_name + ' (contig_name, subject, pident, alignment_length, mismatch, gap_open, contig_start, contig_end, subject_start, subject_end, evalue, bitsocre, contig_coverage, sample_id) values({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13})'.format(
                        contig_name, subject, pident, alignment_length, mismatch, gap_open, q_start, q_end,
                        s_start, s_end, evalue, bitscore, q_coverage, sample_id)
                    print(sql)
                    cur.execute(sql)

                    for taxonId in taxonIds:
                        sql2 = "insert into " + taxon_table + ' (subject, taxon_id) values ({0}, {1})'.format(subject, taxonId)
                        print(sql2)
                        try:
                            cur.execute(sql2)
                        except pg.Error:
                            conn.rollback()
                            continue


cur.close()
conn.close()
