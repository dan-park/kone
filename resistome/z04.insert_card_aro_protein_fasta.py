import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys, getopt


if __name__ == "__main__":

    protein_fa = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["fa="])
    except getopt.GetoptError:
        print('z04.insert_card_aro_protein_fasta.py -i <protein_fasta_protein_homolog_model.fasta>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('z04.insert_card_aro_protein_fasta.py -i <protein_fasta_protein_homolog_model.fasta>')
            sys.exit(1)
        elif opt in ("-i", "--fa"):
            protein_fa = arg

    conn = pg.connect("host=localhost dbname=onehealth user=onehealth password=oh123")
    conn.autocommit = True
    cur = conn.cursor()

    folder = Path(protein_fa)
    table_name = "resistome_proteinmodel"

    for record in SeqIO.parse(folder, "fasta"):
        seq_ids = record.id.split("|")

        protein_acc = "'" + seq_ids[1] + "'"
        aro = "'" + seq_ids[2] + "'"
        gene_name = "'" + seq_ids[3].replace("'", "").replace('"', '') + "'"

        seq_headers_start = record.description.find("[")+1
        seq_headers_end = record.description.find("]")
        taxon_origin = "'"+record.description[seq_headers_start:seq_headers_end]+"'"
        seq_seq = "'"+record.seq+"'"
        seq_length = len(seq_seq) - 2

        sql = "insert into " + table_name + '(protein_acc, aro, protein_name, taxon_origin, length, sequence) values({0}, {1}, {2}, {3}, {4}, {5})'.format(protein_acc, aro, gene_name, taxon_origin, seq_length, seq_seq)
        print(sql)
        cur.execute(sql)


    cur.close()
    conn.close()
