def get_coverage(query, candidates, ppdb):

    do_ppdb = False

    
    n = len(query)
    d = {}
    for candidate in candidates:
        for t in candidate:
            d[t] = 1

    c = 0
    for t in query:
        if t in d:
            c+=1
        elif do_ppdb:
            if t in ppdb:
                if ppdb[t][0] in d:
                    #print t, ppdb[t][0], ppdb[t][1]
                    #print ppdb[t][0] in d
                    c+=1

    return c * 1.0 / n 


def top_n(query, candidates, n, ppdb):
    scores = []
    pre_n , post_n = 3, 0
    for i, candidate in enumerate(candidates):
        if i < pre_n:
            start = 0
        else:
            start = i - pre_n
        if i > len(candidates) - 1 - post_n:
            end = len(candidate) - 1
        else:
            end = i + 1 + post_n
            
        span = candidates[start:end]
        
        score = get_coverage(query, span, ppdb)
        scores.append((i, score))

    scores = sorted(scores, key = lambda x: -x[1])

    return scores[:n]
