
def num_higher_m(ss, s=90):
  num = 0
  for score in ss:
    if score >= s:
      num=num+1
  return num



