with open("scripts/systems/LevelGenerator.gd", "r") as f:
    content = f.read()

# I see what's wrong. I changed ITEMS to a `var` from `const`, but GDScript
# has strict rules about modifying dictionary keys that don't match the initial structure perfectly
# or modifying them during _ready if they hold object references.
# The simplest and most robust way is to just instantiate the dictionary inside the function
# instead of relying on a class-level dictionary.

old_content = """# Item definitions for the generator
var ITEMS = {
	"gold_small": {"scene": null, "value": 50, "radius": 20},
	"gold_large": {"scene": null, "value": 250, "radius": 40},
	"diamond": {"scene": null, "value": 600, "radius": 15},
	"rock": {"scene": null, "value": 10, "radius": 35} # Rocks are hazards, value doesn't count towards budget
}

func _ready() -> void:
	ITEMS["gold_small"]["scene"] = gold_small_scene
	ITEMS["gold_large"]["scene"] = gold_large_scene
	ITEMS["diamond"]["scene"] = diamond_scene
	ITEMS["rock"]["scene"] = rock_scene

func generate_level(level_number: int, target_quota: int) -> void:"""

new_content = """func generate_level(level_number: int, target_quota: int) -> void:
	var ITEMS = {
		"gold_small": {"scene": gold_small_scene, "value": 50, "radius": 20},
		"gold_large": {"scene": gold_large_scene, "value": 250, "radius": 40},
		"diamond": {"scene": diamond_scene, "value": 600, "radius": 15},
		"rock": {"scene": rock_scene, "value": 10, "radius": 35}
	}"""

content = content.replace(old_content, new_content)

# We also need to update _spawn_specific_item to accept the ITEMS dictionary
old_spawn = """func _spawn_specific_item(item_key: String, root: Node, spawned_positions: Array[Vector2], spawn_counts: Dictionary) -> void:
	var data = ITEMS[item_key]"""

new_spawn = """func _spawn_specific_item(item_key: String, root: Node, spawned_positions: Array[Vector2], spawn_counts: Dictionary, ITEMS: Dictionary) -> void:
	var data = ITEMS[item_key]"""

content = content.replace(old_spawn, new_spawn)

# Update the calls to _spawn_specific_item
content = content.replace('_spawn_specific_item(choice, items_root, spawned_positions, spawn_counts)', '_spawn_specific_item(choice, items_root, spawned_positions, spawn_counts, ITEMS)')
content = content.replace('_spawn_specific_item("rock", items_root, spawned_positions, spawn_counts)', '_spawn_specific_item("rock", items_root, spawned_positions, spawn_counts, ITEMS)')


with open("scripts/systems/LevelGenerator.gd", "w") as f:
    f.write(content)
