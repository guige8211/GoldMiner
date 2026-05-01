with open("scripts/Level.gd", "r") as f:
    content = f.read()

# Replace the advance_to_next_level call with a scene transition to Shop
old_code = """	await get_tree().create_timer(2.0).timeout
	GameManager.advance_to_next_level()"""

new_code = """	await get_tree().create_timer(2.0).timeout
	get_tree().change_scene_to_file("res://scenes/Shop.tscn")"""

content = content.replace(old_code, new_code)

with open("scripts/Level.gd", "w") as f:
    f.write(content)
