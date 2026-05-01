import re

with open("scripts/singletons/GameManager.gd", "r") as f:
    content = f.read()

# Fix the bug
old_add = """func add_gold(amount: int) -> void:
	current_gold += amount
	score_changed.emit(current_score)
	coins_changed.emit(current_coins)"""

new_add = """func add_score(amount: int) -> void:
	current_score += amount
	score_changed.emit(current_score)

func add_coins(amount: int) -> void:
	current_coins += amount
	coins_changed.emit(current_coins)"""

content = content.replace(old_add, new_add)

with open("scripts/singletons/GameManager.gd", "w") as f:
    f.write(content)
