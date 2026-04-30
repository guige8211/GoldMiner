extends Node

var meta_resources: int = 0
var unlocked_talents: Dictionary = {
	"base_hook_speed": 0, # Level of the talent
	"starting_gold": 0,
	"shop_discount": 0
}

# Values per talent level
const TALENT_VALUES = {
	"base_hook_speed": 0.05, # +5% per level
	"starting_gold": 50,     # +50 starting gold
	"shop_discount": 0.02    # -2% cost per level
}

const SAVE_PATH = "user://meta_save.res"

func _ready() -> void:
	load_data()

func add_meta_resource(amount: int) -> void:
	meta_resources += amount
	save_data()

func get_talent_value(talent_id: String) -> float:
	if not unlocked_talents.has(talent_id):
		return 0.0
	var level = unlocked_talents[talent_id]
	return level * TALENT_VALUES.get(talent_id, 0.0)

func upgrade_talent(talent_id: String, cost: int) -> bool:
	if meta_resources >= cost:
		meta_resources -= cost
		if unlocked_talents.has(talent_id):
			unlocked_talents[talent_id] += 1
		else:
			unlocked_talents[talent_id] = 1
		save_data()
		return true
	return false

# Basic save/load structure using Godot's built-in tools
func save_data() -> void:
	var file = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_var(meta_resources)
		file.store_var(unlocked_talents)
		file.close()

func load_data() -> void:
	if FileAccess.file_exists(SAVE_PATH):
		var file = FileAccess.open(SAVE_PATH, FileAccess.READ)
		if file:
			meta_resources = file.get_var()
			var loaded_talents = file.get_var()
			if typeof(loaded_talents) == TYPE_DICTIONARY:
				unlocked_talents = loaded_talents
			file.close()
