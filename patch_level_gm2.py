with open("scripts/Level.gd", "r") as f:
    content = f.read()

# Add time skip logic
old_process = """func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("gm_collect_all") or Input.is_key_pressed(KEY_K):
		_gm_collect_all()"""

new_process = """func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("gm_collect_all") or Input.is_key_pressed(KEY_K):
		_gm_collect_all()
	if Input.is_action_just_pressed("gm_time_skip") or Input.is_key_pressed(KEY_T):
		_gm_time_skip()

func _gm_time_skip() -> void:
	if GameManager.is_in_level:
		print("GM: Skipping time to 0!")
		GameManager.time_left = 0.1 # Very close to 0 to let the next tick finish it normally"""

content = content.replace(old_process, new_process)

with open("scripts/Level.gd", "w") as f:
    f.write(content)
