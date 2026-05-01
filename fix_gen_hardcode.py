with open("scripts/systems/LevelGenerator.gd", "r") as f:
    content = f.read()

# Instead of relying on Godot Inspector exports which are constantly breaking due to manual tscn edits,
# let's hardcode the loads in the script directly so it never fails.
old_load = """	var ITEMS = {
		"gold_small": {"scene": gold_small_scene, "value": 50, "radius": 20},
		"gold_large": {"scene": gold_large_scene, "value": 250, "radius": 40},
		"diamond": {"scene": diamond_scene, "value": 600, "radius": 15},
		"rock": {"scene": rock_scene, "value": 10, "radius": 35}
	}"""

new_load = """	var ITEMS = {
		"gold_small": {"scene": load("res://scenes/items/GoldSmall.tscn"), "value": 50, "radius": 20},
		"gold_large": {"scene": load("res://scenes/items/GoldLarge.tscn"), "value": 250, "radius": 40},
		"diamond": {"scene": load("res://scenes/items/Diamond.tscn"), "value": 600, "radius": 15},
		"rock": {"scene": load("res://scenes/items/Rock.tscn"), "value": 10, "radius": 35}
	}"""

content = content.replace(old_load, new_load)

with open("scripts/systems/LevelGenerator.gd", "w") as f:
    f.write(content)
