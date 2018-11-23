import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys
import getopt
import csv


if __name__ == "__main__":

    sample_name = ''
    contig_to_prokka = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:i:", ["sample=", "c2p="])
    except getopt.GetoptError:
        print('z05.insert_contigs_prokka.py -s <samplename> -i <contig_to_prokka.tsv>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('z05.insert_contigs_prokka.py -s <samplename> -i <contig_to_prokka.tsv>')
            sys.exit(1)
        elif opt in ("-s", "--sample"):
            sample_name = arg
        elif opt in ("-i", "--c2p"):
            contig_to_prokka = arg

    print(sample_name)
    print(contig_to_prokka)

    conn = pg.connect("host=localhost dbname=onehealth user=onehealth password=oh123")
    conn.autocommit = True
    cur = conn.cursor()

    folder = Path(contig_to_prokka)
    table_name = "resistome_sampletocontigtolocus"

    sample_id = "'"+sample_name+"'"
    with open(folder) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                contig_name = "'"+row[0]+"'"
                locus_names = row[1].split("|")
                #print(row)
                #print(locus_names)

                for locus_name in locus_names:
                    if len(locus_name)>0:
                        #print(locus_name)
                        locus_name_tkn = "'" + locus_name + "'"
                        sql = "insert into " + table_name + ' (contig_name, locus_name, sample_id) values({0}, {1}, {2})'.format(contig_name, locus_name_tkn, sample_id)
                        print(sql)
                        cur.execute(sql)

    cur.close()
    conn.close()
