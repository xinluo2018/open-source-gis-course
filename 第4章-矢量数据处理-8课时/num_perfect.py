
def get_num_per(scores):
    num_perfect = 0
    for score in scores:
        if score >= 90:
            num_perfect = num_perfect+1
    return num_perfect

# def get_num_low70(scores):
#     num_low70 = 0
#     for score in scores:
#         if score < 70:
#             num_low70 = num_low70+1
#     return num_low70

