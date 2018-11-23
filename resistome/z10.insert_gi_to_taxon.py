import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys
import getopt
import csv


if __name__ == "__main__":

    gi_to_taxon = ''
    gi_num = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:g:", ["gitaxon=", "ginum="])
    except getopt.GetoptError:
        print('z10.insert_gi_to_taxon.py -i <gi_taxon.tsv> -g <ginum.tsv>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('z10.insert_gi_to_taxon.py -i <gi_taxon.tsv> -g <ginum.tsv>')
            sys.exit(1)
        elif opt in ("-i", "--gitaxon"):
            gi_to_taxon = arg
        elif opt in ("-g", "--ginum"):
            gi_num = arg

    print(gi_to_taxon)
    print(gi_num)

    conn = pg.connect("host=localhost dbname=onehealth user=onehealth password=oh123")
    conn.autocommit = True
    cur = conn.cursor()

    folder = Path(gi_to_taxon)
    giList = Path(gi_num)

    giAll = []
    with open(giList, 'r') as gi:
        for row in gi:

            ttk = row.strip()
            if len(ttk) > 0:
                giAll.append(row.strip())

    print("Total: " + str(len(giAll)))

    table_name = "resistome_gitotaxon"

    with open(folder) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")

        t_count = 0
        r_count = 0

        for row in csv_reader:
            gi = row[0]
            taxon = row[1]

            if gi in giAll:
                sql = "insert into " + table_name + ' (gi, taxon) values ({0}, {1})'.format(gi, taxon)
                print(str(t_count) + '\t' + str(r_count) + '\t' + sql)
                cur.execute(sql)
                t_count += 1

            r_count += 1

cur.close()
conn.close()
