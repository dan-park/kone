import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys, getopt


if __name__ == "__main__":

    sample_name = ''
    contig_fa = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:i:", ["sample=", "fa="])
    except getopt.GetoptError:
        print('z01.insert_contigs_into_db.py -s <samplename> -i <contig.fasta>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('z01.insert_contigs_into_db.py -s <samplename> -i <contig.fasta>')
            sys.exit(1)
        elif opt in ("-s", "--sample"):
            sample_name = arg
        elif opt in ("-i", "--fa"):
            contig_fa = arg

    print(sample_name)
    print(contig_fa)

    conn = pg.connect("host=localhost dbname=onehealth user=onehealth password=oh123")
    conn.autocommit = True
    cur = conn.cursor()

    folder = Path(contig_fa)
    table_name = "resistome_sampletocontigs"

    sample_id = "'"+sample_name+"'"
    for record in SeqIO.parse(folder, "fasta"):
        contig_id = "'"+record.id+"'"
        contig_header = "'"+record.description+"'"

        contig_seq = "'"+record.seq+"'"
        contig_length = len(contig_seq)

        sql = "insert into " + table_name + '(contig_name, contig_header, contig_length, contig_seq, sample_id) values({0}, {1}, {2}, {3}, {4})'.format(contig_id, contig_header, contig_length, contig_seq, sample_id)

        print(sql)
        cur.execute(sql)

    cur.close()
    conn.close()
