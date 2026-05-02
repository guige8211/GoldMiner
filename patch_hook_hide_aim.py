with open("scripts/player/Hook.gd", "r") as f:
    content = f.read()

# We only want the AimLine to show when SWINGING. Hide it when EXTENDING or RETRACTING.
old_fire = """func fire() -> void:
	if current_state == HookState.SWINGING:
		current_state = HookState.EXTENDING
		EventBus.hook_fired.emit()"""

new_fire = """func fire() -> void:
	if current_state == HookState.SWINGING:
		current_state = HookState.EXTENDING
		EventBus.hook_fired.emit()
		var aim_line = get_node_or_null("AimLine")
		if aim_line: aim_line.visible = false"""

content = content.replace(old_fire, new_fire)

old_finish = """	grabbed_item = null
	current_state = HookState.SWINGING
	_update_hook_position()"""

new_finish = """	grabbed_item = null
	current_state = HookState.SWINGING
	_update_hook_position()
	var aim_line = get_node_or_null("AimLine")
	if aim_line: aim_line.visible = true"""

content = content.replace(old_finish, new_finish)

with open("scripts/player/Hook.gd", "w") as f:
    f.write(content)
