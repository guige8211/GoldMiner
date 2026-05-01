with open("scripts/systems/LevelGenerator.gd", "r") as f:
    content = f.read()

# Fix the dictionary constant assignment issue in GDScript
old_const = """const ITEMS = {
	"gold_small": {"scene": null, "value": 50, "radius": 20},
	"gold_large": {"scene": null, "value": 250, "radius": 40},
	"diamond": {"scene": null, "value": 600, "radius": 15},
	"rock": {"scene": null, "value": 10, "radius": 35} # Rocks are hazards, value doesn't count towards budget
}

func _ready() -> void:
	ITEMS["gold_small"]["scene"] = gold_small_scene
	ITEMS["gold_large"]["scene"] = gold_large_scene
	ITEMS["diamond"]["scene"] = diamond_scene
	ITEMS["rock"]["scene"] = rock_scene"""

new_var = """var ITEMS = {
	"gold_small": {"scene": null, "value": 50, "radius": 20},
	"gold_large": {"scene": null, "value": 250, "radius": 40},
	"diamond": {"scene": null, "value": 600, "radius": 15},
	"rock": {"scene": null, "value": 10, "radius": 35} # Rocks are hazards, value doesn't count towards budget
}

func _ready() -> void:
	ITEMS["gold_small"]["scene"] = gold_small_scene
	ITEMS["gold_large"]["scene"] = gold_large_scene
	ITEMS["diamond"]["scene"] = diamond_scene
	ITEMS["rock"]["scene"] = rock_scene"""

content = content.replace(old_const, new_var)

with open("scripts/systems/LevelGenerator.gd", "w") as f:
    f.write(content)
