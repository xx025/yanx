import re

ls = re.findall(r"[(](.*?)[)]", "abe(ac)ad)")[-1]
print(ls)
