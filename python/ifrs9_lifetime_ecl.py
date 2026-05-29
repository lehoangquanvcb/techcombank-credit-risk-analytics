def lifetime_pd_curve(pd_12m, years=5, decay=0.85):
    return [min(pd_12m * (decay ** (y-1)), 0.95) for y in range(1, years+1)]

def lifetime_ecl(row, discount_rate=0.08, years=5):
    pds = lifetime_pd_curve(row["pd_12m"], years)
    ecl = 0
    for y, pd_y in enumerate(pds, start=1):
        ecl += pd_y * row["lgd"] * row["ead"] / ((1+discount_rate)**y)
    return ecl
