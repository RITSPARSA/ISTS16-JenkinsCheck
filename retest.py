import re, sys

try:
    string = sys.argv[1]
except:
    string = "++++ Team 3 ++++"

print(re.findall('\d+', string))
