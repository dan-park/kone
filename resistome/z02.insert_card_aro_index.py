import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys
import getopt
import csv

if __name__ == "__main__":

    aro_index = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["input="])
    except getopt.GetoptError:
        print('z02.insert_card_aro_index.py -i <aro_index.csv>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('z02.insert_card_aro_index.py -i <aro_index.csv>')
            sys.exit(1)
        elif opt in ("-i", "--aro"):
            aro_index = arg

    conn = pg.connect("host=localhost dbname=onehealth user=onehealth password=oh123")
    conn.autocommit = True
    cur = conn.cursor()

    folder = Path(aro_index)
    table_name = "resistome_aro"

    with open(folder) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                aro = "'" + row[0] + "'"
                cvterm = row[1]
                model_seq_id = row[2]
                model_id = row[3]
                model_name = "'" + row[4].replace("'", "").replace('"', '') + "'"
                aro_name = "'" + row[5].replace("'", "").replace('"', '') + "'"
                protein_acc = "'" + row[6] + "'"
                dna_acc = "'" + row[7] + "'"

                sql = "insert into " + table_name + '(aro, cvterm, model_sequence_id, model_id, model_name, aro_name, protein_acc, dna_acc) values ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})'.format(aro, cvterm, model_seq_id, model_id, model_name, aro_name, protein_acc, dna_acc)
                print(sql)
                cur.execute(sql)

                line_count += 1

    cur.close()
    conn.close()
