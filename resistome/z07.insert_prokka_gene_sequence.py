import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys
import getopt


if __name__ == "__main__":

    sample_name = ''
    prokka_protein_fa = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:i:", ["sample=", "fa="])
    except getopt.GetoptError:
        print('z07.insert_prokka_gene_sequence.py -s <samplename> -i <protein_prokka.fasta>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('z07.insert_prokka_gene_sequence.py -s <samplename> -i <protein_prokka.fasta>')
            sys.exit(1)
        elif opt in ("-s", "--sample"):
            sample_name = arg
        elif opt in ("-i", "--fa"):
            prokka_protein_fa = arg

    print(sample_name)
    print(prokka_protein_fa)

    conn = pg.connect("host=localhost dbname=onehealth user=onehealth password=oh123")
    conn.autocommit = True
    cur = conn.cursor()

    folder = Path(prokka_protein_fa)
    table_name = "resistome_sampletogeneproteinsequence"

    sample_id = "'"+sample_name+"'"
    for record in SeqIO.parse(folder, "fasta"):
        locus_name = "'"+record.id.replace('"', '').replace("'", "") + "'"
        description = "'"+record.description.replace('"', '').replace("'", "")+"'"

        locus_seq = "'"+record.seq+"'"
        locus_length = len(locus_seq) - 2

        sql = "insert into " + table_name + '(locus_name, description, protein_seq, sample_id) values({0}, {1}, {2}, {3})'.format(locus_name, description, locus_seq, sample_id)

        print(sql)
        cur.execute(sql)

    cur.close()
    conn.close()
