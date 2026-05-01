with open("scripts/Level.gd", "r") as f:
    content = f.read()

# Replace gold_changed with score_changed and coins_changed connections
content = content.replace("GameManager.gold_changed.is_connected(_on_gold_changed)", "GameManager.score_changed.is_connected(_on_score_changed)")
content = content.replace("GameManager.gold_changed.connect(_on_gold_changed)", "GameManager.score_changed.connect(_on_score_changed)\n\t\tGameManager.coins_changed.connect(_on_coins_changed)")

# Replace the initial trigger
content = content.replace("_on_gold_changed(GameManager.current_gold)", "_on_score_changed(GameManager.current_score)\n\t_on_coins_changed(GameManager.current_coins)")

# Replace the handler
old_handler = """func _on_gold_changed(new_gold: int) -> void:
	gold_label.text = "Gold: $%d" % new_gold"""

new_handler = """func _on_score_changed(new_score: int) -> void:
	gold_label.text = "Score: %d" % new_score

func _on_coins_changed(new_coins: int) -> void:
	pass # Could display coins in level too if wanted"""

content = content.replace(old_handler, new_handler)
content = content.replace('quota_label.text = "Target: $%d" % new_quota', 'quota_label.text = "Target: %d" % new_quota')

with open("scripts/Level.gd", "w") as f:
    f.write(content)

with open("scenes/Level.tscn", "r") as f:
    scene = f.read()
scene = scene.replace('text = "Gold: $0"', 'text = "Score: 0"')
scene = scene.replace('text = "Target: $100"', 'text = "Target: 100"')
with open("scenes/Level.tscn", "w") as f:
    f.write(scene)
