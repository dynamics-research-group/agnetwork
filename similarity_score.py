def mcsSimilarityScore(mcs, g1, g2):
    return (len(mcs) * 100) / (len(g1) + len(g2) - len(mcs))