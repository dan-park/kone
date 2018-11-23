import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys
import getopt
import csv


if __name__ == "__main__":

    taxon_names = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["tn="])
    except getopt.GetoptError:
        print('z11.insert_taxon_names.py -i <taxon_names.tsv>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('z11.insert_taxon_names.py -i <taxon_names.tsv>')
            sys.exit(1)
        elif opt in ("-i", "--tn"):
            taxon_names = arg

    print(taxon_names)

    conn = pg.connect("host=localhost dbname=onehealth user=onehealth password=oh123")
    conn.autocommit = True
    cur = conn.cursor()

    folder = Path(taxon_names)

    table_name = "resistome_taxondb"

    with open(folder) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="|")
        for row in csv_reader:
            taxon_id = row[0].strip()
            taxon_name = "'" + row[1].strip().replace("'", "").replace('"', '') + "'"
            taxon_unique = "'" + row[2].strip().replace("'", "").replace('"', '') + "'"
            taxon_name_class = "'" + row[3].strip() + "'"

            if row[3].strip().startswith('scientific name'):
                #print(taxon_id)
                #print(taxon_name)
                #print(taxon_unique)
                #print(taxon_name_class)
                #print("--")

                sql = "insert into " + table_name + ' (taxon_id, taxon_name, taxon_unique, taxon_name_class) values ({0}, {1}, {2}, {3})'.format(taxon_id, taxon_name, taxon_unique, taxon_name_class)
                print(sql)

                cur.execute(sql)


cur.close()
conn.close()
