extends Node
class_name LevelGenerator

@export var spawn_area_min: Vector2 = Vector2(50, 200)
@export var spawn_area_max: Vector2 = Vector2(1230, 650)
@export var items_root_path: NodePath

# In a real game, these would be PackedScenes
# @export var gold_scene: PackedScene
# @export var rock_scene: PackedScene
# @export var diamond_scene: PackedScene
# @export var chest_scene: PackedScene

func generate_level(level_number: int) -> void:
	# Clear existing items
	var items_root = get_node(items_root_path)
	if items_root:
		for child in items_root.get_children():
			child.queue_free()
	
	# Determine difficulty/spawn counts based on level
	var num_gold = 5 + randi() % 3
	var num_rocks = 2 + int(level_number * 0.8) # More rocks as levels increase
	
	# Diamonds have base chance + upgrade bonus
	var diamond_chance = 0.1 + (level_number * 0.05) + UpgradeManager.diamond_spawn_chance_bonus
	var num_diamonds = 0
	if randf() < diamond_chance:
		num_diamonds = 1 + randi() % 2
		
	var chest_chance = 0.2 + (level_number * 0.02)
	var num_chests = 0
	if randf() < chest_chance:
		num_chests = 1
		
	# _spawn_items(gold_scene, num_gold, items_root)
	# _spawn_items(rock_scene, num_rocks, items_root)
	# _spawn_items(diamond_scene, num_diamonds, items_root)
	# _spawn_items(chest_scene, num_chests, items_root)
	
	print("Level %d Generated: %d Gold, %d Rocks, %d Diamonds, %d Chests" % [level_number, num_gold, num_rocks, num_diamonds, num_chests])

func _spawn_items(scene: PackedScene, count: int, root: Node) -> void:
	if not scene or not root:
		return
		
	for i in range(count):
		var item = scene.instantiate()
		# Basic random position, in a real game we'd use Poisson Disk Sampling 
		# or overlap checks to prevent items from stacking directly on top of each other
		item.position = Vector2(
			randf_range(spawn_area_min.x, spawn_area_max.x),
			randf_range(spawn_area_min.y, spawn_area_max.y)
		)
		root.add_child(item)
