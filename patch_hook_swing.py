with open("scripts/player/Hook.gd", "r") as f:
    content = f.read()

# Apply the hook_swing_multiplier
old_swing = """func _process_swing(delta: float) -> void:
	# Modulate swing speed based on upgrades if needed
	var actual_swing_speed = swing_speed * UpgradeManager.hook_speed_multiplier"""

new_swing = """func _process_swing(delta: float) -> void:
	# Modulate swing speed based on upgrades if needed
	var actual_swing_speed = swing_speed * UpgradeManager.hook_speed_multiplier * UpgradeManager.hook_swing_multiplier"""

content = content.replace(old_swing, new_swing)

with open("scripts/player/Hook.gd", "w") as f:
    f.write(content)
