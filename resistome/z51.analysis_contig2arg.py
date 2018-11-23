import psycopg2 as pg
import intervals as I

if __name__ == "__main__":

    conn = pg.connect("host=localhost dbname=onehealth user=onehealth password=oh123")
    conn.autocommit = True
    cur = conn.cursor()

    sql = "select ca.contig_name, ca.pident, ca.aln_length, ca.aro_start, ca.aro_end, aro.aro, aro.aro_name, aro.protein_acc, protein.length from resistome_contigtoaro as ca, resistome_aro as aro, resistome_proteinmodel as protein where pident>80 and ca.aro = aro.aro and aro.protein_acc = protein.protein_acc order by pident desc"



    print(sql)
    cur.execute(sql)
    query_results = cur.fetchall()

    aro_to_top = {}
    for result in query_results:

        if result[5] in aro_to_top:
            aro_to_top[result[5]].append(result)
        else:
            aro_to_top[result[5]] = [result]

    aro_coverage = {}
    for aro in aro_to_top:
        mappings = aro_to_top[aro]
        mapping_intervals = []
        union_interval = None
        aro_length = None

        for map_r in mappings:
            aro_start = map_r[3]
            aro_end = map_r[4]
            #print(map_r)
            coverage_interval = I.closed(aro_start, aro_end)
            mapping_intervals.append(coverage_interval)

            if union_interval is None:
                union_interval = I.closed(aro_start, aro_end)
            else:
                union_interval = union_interval | coverage_interval

            if aro_length:
                aro_length = map_r[8]

        covered = 0
        for interval in union_interval:
            covered_interval = interval.upper - interval.lower + 1
            covered += covered_interval

        coverageRatio = float(covered) / float(map_r[8])
        aro_coverage[aro] = coverageRatio
        #print(coverageRatio)


    aro_coverage_so = sorted(aro_coverage, key=lambda aro : aro_coverage[aro], reverse=True)
    print(aro_coverage_so)
    for aro in aro_coverage_so:
        mappings = aro_to_top[aro]
        gene = None
        geneAcc = None
        geneLength = None

        weighted_identity = 0
        for map_r in mappings:
            gene = map_r[6]
            geneAcc = map_r[7]
            geneLength = map_r[8]

            #print(map_r)
        print(aro + '\t' + gene + "\t" + geneAcc + '\t' + str(geneLength) + '\t' + str(len(mappings)) + '\t'+ str(aro_coverage[aro]))

    cur.close()
    conn.close()

