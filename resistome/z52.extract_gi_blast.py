import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys
import getopt
import csv


if __name__ == "__main__":

    sample_name = ''
    contig_to_blast = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:i:", ["sample=", "c2b="])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            sys.exit(1)
        elif opt in ("-s", "--sample"):
            sample_name = arg
        elif opt in ("-i", "--contig2blast"):
            contig_to_blast = arg

    print(sample_name)
    print(contig_to_blast)

    folder = Path(contig_to_blast)

    sample_id = "'"+sample_name+"'"
    with open(folder) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")

        queryId = None
        queryLength = None

        gi_to_accession = {}
        for row in csv_reader:
            if row[0].startswith("# Query"):
                queryInfo = row[0].split(" ")
                queryId = queryInfo[2]
                queryLength = int(queryInfo[5].replace("len=", ""))

            elif not row[0].startswith("#"):
                subject = row[1]
                tkns = subject.split("|")
                gi_number = tkns[1]
                gi_to_accession[gi_number] = 'Y'

        with open("gi_numbers.txt", 'w') as wf:
            for k in gi_to_accession:
                wf.write(k+"\n")


