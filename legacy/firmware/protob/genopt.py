import re
import sys

messageRe = re.compile(r"message (Ripple\w+) {")
fieldRe = re.compile(r"(repeated|optional) (\w+) (\w+) = \d+;")
message = ""
field = ""
outs = []
maxPathLen = 0
f = open(sys.argv[1])
line = f.readline()
while line:
    line = f.readline()
    resM = messageRe.search(line)
    if resM is not None:
        resM = resM.groups()
        message = resM[0]

    resF = fieldRe.search(line)
    if resF is not None:
        resF = resF.groups()
        path = "{}.{}".format(message, resF[2])
        maxPathLen = max(maxPathLen, len(path))
        if resF[0] == "repeated":
            maxSize = str(int(input(path + " : (count) ")))
            outs.append((path, "max_count:" + maxSize))
        if resF[1] == "string" or resF[1] == "bytes":
            maxSize = str(int(input(path + " : (size) ")))
            outs.append((path, "max_size:" + maxSize))
f.close()

for l in outs:
    ll = len(l[0])

    print(l[0] + " " * (maxPathLen - ll + 1) + l[1])
