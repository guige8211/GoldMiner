with open("scripts/player/Player.gd", "r") as f:
    content = f.read()

# We can bypass the custom input map if it keeps failing by just using standard inputs
# or physical keys to ensure it works 100% without project.godot relying on weird formats.
old_input = """	if Input.is_action_just_pressed("ui_accept") or Input.is_action_just_pressed("drop_hook"):
		if hook.current_state == hook.HookState.SWINGING:"""

new_input = """	if Input.is_action_just_pressed("ui_accept") or Input.is_key_pressed(KEY_SPACE) or Input.is_key_pressed(KEY_DOWN):
		if hook.current_state == hook.HookState.SWINGING:"""

content = content.replace(old_input, new_input)

with open("scripts/player/Player.gd", "w") as f:
    f.write(content)
