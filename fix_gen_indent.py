with open("scripts/systems/LevelGenerator.gd", "r") as f:
    content = f.read()

# I found it. Oh my god. The indentation error on queue_free.
# When I added the debug prints:
#	if items_root:
#		print("Items root found")
#	else:
#		print("ERROR: Items root NOT found!")
#		return
#		for child in items_root.get_children():
#			child.queue_free()
#
# The loop to clear items AND generate new ones is perfectly indented
# But the queue_free was placed inside the else block due to bad indentation!
# WAIT NO. The generation while loop IS correctly indented.
# BUT look at `if not scene: return` inside `_spawn_specific_item`.
# Is `scene` actually valid?
# Let's add a debug print to see if `scene` is null!

debug_spawn = """func _spawn_specific_item(item_key: String, root: Node, spawned_positions: Array[Vector2], spawn_counts: Dictionary, ITEMS: Dictionary) -> void:
	var data = ITEMS[item_key]
	var scene = data["scene"] as PackedScene
	if not scene:
		print("ERROR: Scene for ", item_key, " is NULL! Did you assign it in the inspector?")
		return"""

content = content.replace("""func _spawn_specific_item(item_key: String, root: Node, spawned_positions: Array[Vector2], spawn_counts: Dictionary, ITEMS: Dictionary) -> void:
	var data = ITEMS[item_key]
	var scene = data["scene"] as PackedScene
	if not scene:
		return""", debug_spawn)

with open("scripts/systems/LevelGenerator.gd", "w") as f:
    f.write(content)
