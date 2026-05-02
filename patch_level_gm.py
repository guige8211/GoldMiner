with open("scripts/Level.gd", "r") as f:
    content = f.read()

# Add _process to listen for GM keys
gm_code = """
func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("gm_collect_all") or Input.is_key_pressed(KEY_K):
		_gm_collect_all()

func _gm_collect_all() -> void:
	var items_root = get_node_or_null("ItemsRoot")
	if not items_root: return
	
	print("GM: Collecting all valuable items!")
	for child in items_root.get_children():
		if child.has_method("collect") and child.get("type") != 1: # 1 is ROCK
			child.collect()
			child.queue_free()
"""

# Insert right after _ready
content = content.replace("func _on_score_changed", gm_code + "\nfunc _on_score_changed")

with open("scripts/Level.gd", "w") as f:
    f.write(content)
