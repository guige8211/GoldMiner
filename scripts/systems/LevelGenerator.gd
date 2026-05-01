extends Node
class_name LevelGenerator

@export var spawn_area_min: Vector2 = Vector2(100, 250)
@export var spawn_area_max: Vector2 = Vector2(1180, 650)
@export var items_root_path: NodePath

@export var gold_small_scene: PackedScene
@export var gold_large_scene: PackedScene
@export var rock_scene: PackedScene
@export var diamond_scene: PackedScene

# Meta K value (currently 1.5 to give the player 50% more value than needed to pass)
var base_k_factor: float = 1.5

# Item definitions for the generator
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

func generate_level(level_number: int, target_quota: int) -> void:
	var items_root = get_node(items_root_path)
	if items_root:
		for child in items_root.get_children():
			child.queue_free()
	
	# 1. Calculate Value Budget
	# In the future, K will decrease as meta-progression gives players passive bonuses
	var actual_k = base_k_factor 
	var value_budget = target_quota * actual_k
	var current_value = 0
	
	var spawned_positions: Array[Vector2] = []
	var spawn_counts = {"gold_small": 0, "gold_large": 0, "diamond": 0, "rock": 0}
	
	# 2. Define Difficulty Curve & Weights
	# High weight means more likely to be picked for the budget
	var weight_large = max(10, 80 - (level_number * 5)) # Drops as level goes up
	var weight_small = 40 # Relatively stable
	var weight_diamond = min(50, 5 + (level_number * 4)) # Rises as level goes up
	
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
			
		_spawn_specific_item(choice, items_root, spawned_positions, spawn_counts)
		current_value += ITEMS[choice]["value"]
	
	# 3. Spawn Hazards (Rocks) based on difficulty
	# Rocks act as physical blockers. The higher the level, the more rocks.
	var num_rocks = 2 + int(level_number * 1.5) + (randi() % 3)
	for i in range(num_rocks):
		_spawn_specific_item("rock", items_root, spawned_positions, spawn_counts)
	
	print("Level %d Generated. Quota: $%d | Total Value on field: $%d" % [level_number, target_quota, current_value])
	print("Spawns: ", spawn_counts)

func _spawn_specific_item(item_key: String, root: Node, spawned_positions: Array[Vector2], spawn_counts: Dictionary) -> void:
	var data = ITEMS[item_key]
	var scene = data["scene"] as PackedScene
	if not scene:
		return
		
	var item = scene.instantiate()
	var pos = _find_valid_position(spawned_positions, data["radius"])
	item.position = pos
	
	root.add_child(item)
	spawned_positions.append(pos)
	spawn_counts[item_key] += 1

func _find_valid_position(existing_positions: Array[Vector2], required_radius: float) -> Vector2:
	var max_attempts = 50
	
	for attempt in range(max_attempts):
		var test_pos = Vector2(
			randf_range(spawn_area_min.x, spawn_area_max.x),
			randf_range(spawn_area_min.y, spawn_area_max.y)
		)
		
		var is_valid = true
		for pos in existing_positions:
			# Simple distance check to prevent complete overlapping
			# We use a base safe distance of 40 pixels + the item's own radius
			if test_pos.distance_to(pos) < (30 + required_radius):
				is_valid = false
				break
				
		if is_valid:
			return test_pos
			
	# Fallback if too crowded (just force spawn it)
	return Vector2(
		randf_range(spawn_area_min.x, spawn_area_max.x),
		randf_range(spawn_area_min.y, spawn_area_max.y)
	)
