
def num_higher(scores, s_high):
    num = 0
    for score in scores:
        if score >= s_high:
            num=num+1
    return num

def num_lower(scores, s_low):
    num = 0
    for score in scores:
        if score < s_low:
            num=num+1
    return num
