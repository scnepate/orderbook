eps = 1e-12

def compare(a, b):
    if not a and not b:
        return 0
    if abs(a - b) <= eps:
        return 0
    if a < b:
        return -1
    if a > b:
        return 1
    

# add BIDS_STR, ASKS_STR