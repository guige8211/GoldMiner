# Ah, I see what happened. In step "Implement Logic in UpgradeManager.gd and Core Scripts"
# I completely botched the patch file. 
# `UpgradeManager.gd` in the filesystem got mangled because it lost `has_upgrade()`, `add_upgrade()`,
# `_on_item_collected`, etc., which I had written in an earlier step!
# My previous Python string replace command found multiple instances or overwrote half the file.
# Let's completely rewrite UpgradeManager.gd to be correct and clean.

full_content = """extends Node

var hook_speed_multiplier: float = 1.0
var hook_swing_multiplier: float = 1.0
var hook_extend_speed_multiplier: float = 1.0
var diamond_spawn_chance_bonus: float = 0.0

var active_items: Array = []
var combo_count: int = 0

func _ready() -> void:
	EventBus.item_collected.connect(_on_item_collected)
	EventBus.request_item_value_modifiers.connect(_on_request_value_modifiers)
	EventBus.request_retract_speed_modifiers.connect(_on_request_retract_modifiers)
	EventBus.hook_fired.connect(_on_hook_fired)

func _is_match(item: Node2D, target_type: int, target_name: String) -> bool:
	if has_upgrade("wildcard"): return true
	if target_type != -1 and item.get("type") == target_type: return true
	if target_name != "" and item.get("item_name") == target_name: return true
	return false

func reset_run() -> void:
	hook_speed_multiplier = 1.0
	hook_swing_multiplier = 1.0
	hook_extend_speed_multiplier = 1.0
	diamond_spawn_chance_bonus = 0.0
	active_items.clear()
	combo_count = 0
	_apply_meta_progression()

func _apply_meta_progression() -> void:
	hook_speed_multiplier += MetaProgression.get_talent_value("base_hook_speed")

func has_upgrade(id: String) -> bool:
	return active_items.has(id)

func add_upgrade(id: String) -> void:
	if has_upgrade(id):
		return
		
	active_items.append(id)
	var data = ItemDB.get_upgrade(id)
	
	if data.get("type") == "static":
		var stat = data.get("stat")
		var val = data.get("value")
		if stat and val != null:
			set(stat, get(stat) + val)
			
	if id == "greedy_pot":
		GameManager.interest_cap = 15

func _on_item_collected(item: Node2D) -> void:
	if has_upgrade("metronome"):
		combo_count += 1
	
	if has_upgrade("pocket_watch"):
		GameManager.time_left += 2.0
		GameManager.timer_updated.emit(GameManager.time_left)
		
	if has_upgrade("gold_rush") and _is_match(item, -1, "Small Gold"):
		GameManager.add_coins(1)
		
	if has_upgrade("adrenaline") and _is_match(item, 1, ""):
		GameManager.time_left = max(0.1, GameManager.time_left - 5.0)

func _on_request_value_modifiers(item: Node2D, context: Dictionary) -> void:
	if has_upgrade("geologist") and _is_match(item, 1, ""):
		context["base_value"] = 80
		
	if has_upgrade("appraisal"):
		context["base_value"] += 30
	
	if has_upgrade("finale") and GameManager.time_left <= 10.0:
		context["multiplier"] *= 2.0

func _on_request_retract_modifiers(item: Node2D, context: Dictionary) -> void:
	if has_upgrade("metronome"):
		var speed_bonus = combo_count * 0.1
		context["speed_multiplier"] += speed_bonus
		
	if has_upgrade("rock_crusher") and _is_match(item, 1, ""):
		context["speed_multiplier"] += 1.5

func _on_hook_fired() -> void:
	if has_upgrade("adrenaline"):
		hook_extend_speed_multiplier = 1.4
	else:
		hook_extend_speed_multiplier = 1.0
"""

with open("scripts/singletons/UpgradeManager.gd", "w") as f:
    f.write(full_content)
