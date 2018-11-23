import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys
import getopt
import csv

if __name__ == "__main__":

    aro_categories_index = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["input="])
    except getopt.GetoptError:
        print('z03.insert_card_aro_categories.py -i <aro_categories_index.csv>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('z02.insert_card_aro_categories.py -i <aro_categories_index.csv>')
            sys.exit(1)
        elif opt in ("-i", "--aro"):
            aro_categories_index = arg

    conn = pg.connect("host=localhost dbname=onehealth user=onehealth password=oh123")
    conn.autocommit = True
    cur = conn.cursor()

    folder = Path(aro_categories_index)
    table_name_gf = "resistome_arogenefamily"
    table_name_dc = "resistome_arodrugclass"
    table_name_rm = "resistome_aroresistancemechanism"

    with open(folder) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                print(row)
                protein_acc = "'"+row[0]+"'"
                dna_acc = "'"+row[1]+"'"
                gene_families = row[2].replace("'", "").replace('"', '').split(";")
                drug_classes = row[3].replace("'", "").replace('"', '').split(";")
                resistance_mechanisms = row[4].replace("'", "").replace('"', '').split(";")

                # gene family
                for gene_family in gene_families:

                    gene_family_tkn = "'"+gene_family+"'"
                    sql = "insert into " + table_name_gf + ' (protein_acc, dna_acc, amr_gene_family) values ({0}, {1}, {2})'.format(protein_acc, dna_acc, gene_family_tkn)
                    print(sql)
                    cur.execute(sql)

                # drug class
                for drug_class in drug_classes:

                    drug_class_tkn = "'"+drug_class+"'"
                    sql = "insert into " + table_name_dc + ' (protein_acc, dna_acc, amr_drug_class) values ({0}, {1}, {2})'.format(protein_acc, dna_acc, drug_class_tkn)
                    print(sql)
                    cur.execute(sql)

                # resistance mechanism
                for resistance_mechanism in resistance_mechanisms:

                    resistance_mechanism_tkn = "'"+resistance_mechanism+"'"
                    sql = "insert into " + table_name_rm + ' (protein_acc, dna_acc, amr_resistance_mechanism) values ({0}, {1}, {2})'.format(protein_acc, dna_acc, resistance_mechanism_tkn)
                    print(sql)
                    cur.execute(sql)

                line_count += 1

    cur.close()
    conn.close()
