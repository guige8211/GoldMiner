with open("scripts/systems/LevelGenerator.gd", "r") as f:
    content = f.read()

# I need to ensure that the logic correctly picks up the exports and adds them to the node tree
# Let's add debug prints to generate_level to see what's failing silently

debug_prints = """	print("Generating level: ", level_number, " with quota: ", target_quota)
	if items_root:
		print("Items root found")
	else:
		print("ERROR: Items root NOT found!")
		return"""

content = content.replace("	if items_root:", debug_prints)

with open("scripts/systems/LevelGenerator.gd", "w") as f:
    f.write(content)
