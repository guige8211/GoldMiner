extends Node

# Active modifiers for the current run
var hook_speed_multiplier: float = 1.0
var hook_swing_multiplier: float = 1.0
var hook_extend_speed_multiplier: float = 1.0
var gold_value_multiplier: float = 1.0
var rock_value_multiplier: float = 1.0
var diamond_spawn_chance_bonus: float = 0.0

var active_items: Array = []
var pending_chests: int = 0

signal modifiers_updated


func _is_match(item: Node2D, target_type: int, target_name: String) -> bool:
	if has_upgrade("wildcard"): return true
	if target_type != -1 and item.get("type") == target_type: return true
	if target_name != "" and item.get("item_name") == target_name: return true
	return false

func reset_run() -> void:
	hook_speed_multiplier = 1.0
	hook_swing_multiplier = 1.0
	hook_extend_speed_multiplier = 1.0
	gold_value_multiplier = 1.0
	rock_value_multiplier = 1.0
	diamond_spawn_chance_bonus = 0.0
	active_items.clear()
	pending_chests = 0
	
	_apply_meta_progression()
	modifiers_updated.emit()

func _apply_meta_progression() -> void:
	# Add base stats from permanent talents
	hook_speed_multiplier += MetaProgression.get_talent_value("base_hook_speed")
	# More to be added

func add_pending_chest() -> void:
	pending_chests += 1

func open_chest() -> Dictionary:
	if pending_chests <= 0:
		return {}
	pending_chests -= 1
	
	# Mock random item generation
	# In a real game, this would query an item database with drop weights
	var item = {
		"name": "Speedy Gear",
		"type": "stat_boost",
		"stat": "hook_speed_multiplier",
		"value": 0.1
	}
	_apply_item(item)
	return item

func _apply_item(item: Dictionary) -> void:
	active_items.append(item)
	if item.has("stat") and item.has("value"):
		set(item["stat"], get(item["stat"]) + item["value"])
	modifiers_updated.emit()
