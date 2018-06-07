import os
import sys

def extract_ppdb(fn):
    fppdb = open(fn)

    d = {}

    for line in fppdb:
        ll = line.split(' ||| ')
        f = ll[1]
        e = ll[2]
        pfe = ll[3].split()[-2]
        assert(pfe.startswith('p(f|e)='))
        pfe = float(pfe.split('=')[-1])

        if f not in d:
            d[f] = [e,pfe]
        else:
            old_pfe = d[f][1]
            if pfe < old_pfe:
                d[f] = [e,pfe]

    #for f in d:
    #    e, pfe = d[f]
    #    print f, e, pfe
    
    fppdb.close()

    return d
