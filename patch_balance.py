with open("scripts/systems/LevelGenerator.gd", "r") as f:
    content = f.read()

# Make Level 1 much easier by removing rocks and adding base spawns
old_loop = """	# Loop until our spawned items reach the required budget
	while current_value < value_budget:
		var total_weight = weight_large + weight_small + weight_diamond
		var roll = randi() % total_weight
		
		var choice = ""
		if roll < weight_large:
			choice = "gold_large"
		elif roll < weight_large + weight_small:
			choice = "gold_small"
		else:
			choice = "diamond"
			
		_spawn_specific_item(choice, items_root, spawned_positions, spawn_counts, ITEMS)
		current_value += ITEMS[choice]["value"]
	
	# 3. Spawn Hazards (Rocks) based on difficulty
	# Rocks act as physical blockers. The higher the level, the more rocks.
	var num_rocks = 2 + int(level_number * 1.5) + (randi() % 3)
	for i in range(num_rocks):
		_spawn_specific_item("rock", items_root, spawned_positions, spawn_counts, ITEMS)"""

new_loop = """	# 2.5 Force Easy Start for Level 1
	if level_number == 1:
		for i in range(3):
			_spawn_specific_item("gold_small", items_root, spawned_positions, spawn_counts, ITEMS)
			current_value += ITEMS["gold_small"]["value"]

	# Loop until our spawned items reach the required budget
	while current_value < value_budget:
		var total_weight = weight_large + weight_small + weight_diamond
		var roll = randi() % total_weight
		
		var choice = ""
		if roll < weight_large:
			choice = "gold_large"
		elif roll < weight_large + weight_small:
			choice = "gold_small"
		else:
			choice = "diamond"
			
		_spawn_specific_item(choice, items_root, spawned_positions, spawn_counts, ITEMS)
		current_value += ITEMS[choice]["value"]
	
	# 3. Spawn Hazards (Rocks) based on difficulty
	# Rocks act as physical blockers. The higher the level, the more rocks.
	# Level 1 has NO rocks.
	var num_rocks = 0
	if level_number > 1:
		num_rocks = 1 + int(level_number * 1.2) + (randi() % 2)
		for i in range(num_rocks):
			_spawn_specific_item("rock", items_root, spawned_positions, spawn_counts, ITEMS)"""

content = content.replace(old_loop, new_loop)

with open("scripts/systems/LevelGenerator.gd", "w") as f:
    f.write(content)
