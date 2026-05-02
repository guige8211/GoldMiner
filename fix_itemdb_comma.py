with open("scripts/data/ItemDB.gd", "r") as f:
    content = f.read()

# I see the error: "Parse Error: Expected closing "}" after dictionary elements."
# at line 118.
# Look at the end of compound_interest:
# 	"compound_interest": {
#		"name": "资本复利",
#		"desc": "利息不再受上限限制，而是按你当前总资产的 10% 直接发放分红！",
#		"price": 20,
#		"type": "dynamic",
#		"color": Color(1.0, 0.8, 0.4)
#	}
#
#	"metronome": {
# It is MISSING A COMMA between compound_interest and metronome!

content = content.replace('\t}\n\n\t"metronome"', '\t},\n\t"metronome"')

with open("scripts/data/ItemDB.gd", "w") as f:
    f.write(content)
