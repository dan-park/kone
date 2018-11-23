import psycopg2 as pg
from Bio import SeqIO
from pathlib import Path
import sys
import getopt
import csv


if __name__ == "__main__":

    sample_name = ''
    contig_to_blast = ''
    q_coverage_ratio_thr = 0.8

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
    table_name = "resistome_contigtoblastresult"

    sample_id = "'"+sample_name+"'"
    with open(folder) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")

        queryId = None
        queryLength = None

        for row in csv_reader:
            if row[0].startswith("# Query"):
                queryInfo = row[0].split(" ")
                queryId = queryInfo[2]
                queryLength = int(queryInfo[5].replace("len=", ""))
                #print(queryId)

            elif not row[0].startswith("#"):
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

                q_coverage = abs(q_end - q_start) + 1
                q_coverage_ratio = float(q_coverage) / float(queryLength)

                if q_coverage_ratio >= q_coverage_ratio_thr:
                    sql = "insert into " + table_name + ' (contig_name, subject, pident, alignment_length, mismatch, gap_open, contig_start, contig_end, subject_start, subject_end, evalue, bitsocre, sample_id) values({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12})'.format(
                        contig_name, subject, pident, alignment_length, mismatch, gap_open, q_start, q_end, s_start, s_end,
                        evalue, bitscore, sample_id)
                    print(sql)
                    cur.execute(sql)

                    #sql = ""
                    #print(q_coverage_ratio)


        #for row in csv_reader:
        #    contig_name = "'"+row[0]+"'"
        #    aro_infos = row[1].split("|")
        #    aro = "'" + aro_infos[2] + "'"
        #    pident = row[2]
        #    aln_length = row[3]
        ##    num_mismatch = row[4]
        #    gap_open = row[5]
        #    qstart = row[6]
        #    qend = row[7]
        #    aro_start = row[8]
        #    aro_end = row[9]
        #    evalue = row[10]
        #    bitscore = row[11]

        #    sql = "insert into " + table_name + ' (contig_name, aro, pident, aln_length, num_mismatch, gap_open, qstart, qend, aro_start, aro_end, evalue, bitscore, sample_id) values({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12})'.format(contig_name, aro, pident, aln_length, num_mismatch, gap_open, qstart, qend, aro_start, aro_end, evalue, bitscore, sample_id)
        #    print(sql)
        #    cur.execute(sql)

cur.close()
conn.close()
