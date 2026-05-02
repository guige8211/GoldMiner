import re

with open("scripts/singletons/UpgradeManager.gd", "r") as f:
    content = f.read()

# 1. Add hook_swing_multiplier and init logic
content = content.replace("var hook_speed_multiplier: float = 1.0", "var hook_speed_multiplier: float = 1.0\nvar hook_swing_multiplier: float = 1.0")
content = content.replace("hook_speed_multiplier = 1.0", "hook_speed_multiplier = 1.0\n\thook_swing_multiplier = 1.0")

# 2. Add EventBus.hook_fired listener for Adrenaline
content = content.replace("EventBus.request_retract_speed_modifiers.connect(_on_request_retract_modifiers)", "EventBus.request_retract_speed_modifiers.connect(_on_request_retract_modifiers)\n\tEventBus.hook_fired.connect(_on_hook_fired)")

# 3. Add Wildcard helper function
wildcard_helper = """
func _is_match(item: Node2D, target_type: int, target_name: String) -> bool:
	if has_upgrade("wildcard"): return true
	if target_type != -1 and item.get("type") == target_type: return true
	if target_name != "" and item.get("item_name") == target_name: return true
	return false
"""
content = content.replace("func reset_run() -> void:", wildcard_helper + "\nfunc reset_run() -> void:")

# 4. Modify existing logic to use _is_match
old_val = """	# Geologist Logic
	if has_upgrade("geologist") and item.get("type") == 1: # 1 is ROCK
		context["base_value"] = 80 # Override base value completely"""
new_val = """	# Geologist Logic
	if has_upgrade("geologist") and _is_match(item, 1, ""): # 1 is ROCK
		context["base_value"] = 80 # Override base value completely"""
content = content.replace(old_val, new_val)

old_rush = """	# Gold Rush Logic
	if has_upgrade("gold_rush") and item.item_name == "Small Gold":
		GameManager.add_coins(1)"""
new_rush = """	# Gold Rush Logic
	if has_upgrade("gold_rush") and _is_match(item, -1, "Small Gold"):
		GameManager.add_coins(1)
		
	# Adrenaline Penalty Logic
	if has_upgrade("adrenaline") and item.get("type") == 1:
		GameManager.time_left = max(0.1, GameManager.time_left - 5.0)"""
content = content.replace(old_rush, new_rush)


# 5. Add Adrenaline and Rock Crusher hooks
old_retract = """	if has_upgrade("metronome"):
		var speed_bonus = combo_count * 0.1
		context["speed_multiplier"] += speed_bonus"""
new_retract = """	if has_upgrade("metronome"):
		var speed_bonus = combo_count * 0.1
		context["speed_multiplier"] += speed_bonus
		
	# Rock Crusher Logic
	if has_upgrade("rock_crusher") and item.get("type") == 1:
		context["speed_multiplier"] += 1.5 # 50% faster + counteracts the 0.5 rock penalty naturally
		
func _on_hook_fired() -> void:
	# Adrenaline Buff
	if has_upgrade("adrenaline"):
		hook_extend_speed_multiplier = 1.4
	else:
		hook_extend_speed_multiplier = 1.0"""
content = content.replace(old_retract, new_retract)

with open("scripts/singletons/UpgradeManager.gd", "w") as f:
    f.write(content)
