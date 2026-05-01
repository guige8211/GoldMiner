with open("scripts/systems/LevelGenerator.gd", "r") as f:
    content = f.read()

# Make Level 1 MUCH denser with large targets
old_loop = """	# 2.5 Force Easy Start for Level 1
	if level_number == 1:
		for i in range(3):
			_spawn_specific_item("gold_small", items_root, spawned_positions, spawn_counts, ITEMS)
			current_value += ITEMS["gold_small"]["value"]"""

new_loop = """	# 2.5 Force Easy Start for Level 1
	if level_number == 1:
		for i in range(5):
			_spawn_specific_item("gold_small", items_root, spawned_positions, spawn_counts, ITEMS)
			current_value += ITEMS["gold_small"]["value"]
		for i in range(3):
			_spawn_specific_item("gold_large", items_root, spawned_positions, spawn_counts, ITEMS)
			current_value += ITEMS["gold_large"]["value"]"""

content = content.replace(old_loop, new_loop)

with open("scripts/systems/LevelGenerator.gd", "w") as f:
    f.write(content)
