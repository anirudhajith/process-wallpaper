import re

treeFile = open("tree", "r")

jsonString = "["

for line in treeFile:
    line = re.sub(r"[\s - \|]", "", line, flags=re.UNICODE)
    line = re.sub(r"\-\+\-", "+", line, flags=re.UNICODE)
    print(line)