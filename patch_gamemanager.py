import re

with open("scripts/singletons/GameManager.gd", "r") as f:
    content = f.read()

# 1. Replace variables and signals
content = content.replace("signal gold_changed(new_gold)", "signal score_changed(new_score)\nsignal coins_changed(new_coins)")
content = content.replace("var current_gold: int = 0", "var current_score: int = 0\nvar current_coins: int = 0\nvar interest_cap: int = 5")

# 2. Fix start_new_run to reset coins
old_start = """func start_new_run() -> void:
	UpgradeManager.reset_run()
	current_gold = 0
	current_level = 1"""

new_start = """func start_new_run() -> void:
	UpgradeManager.reset_run()
	current_score = 0
	current_coins = 0
	interest_cap = 5
	current_level = 1"""

content = content.replace(old_start, new_start)

# Update the signals emitted in start_new_run
content = content.replace("gold_changed.emit(current_gold)", "score_changed.emit(current_score)\n\tcoins_changed.emit(current_coins)")

# 3. Update add_gold to add_score
old_add = """func add_gold(amount: int) -> void:
	current_gold += amount
	gold_changed.emit(current_gold)"""

new_add = """func add_score(amount: int) -> void:
	current_score += amount
	score_changed.emit(current_score)

func add_coins(amount: int) -> void:
	current_coins += amount
	coins_changed.emit(current_coins)"""

content = content.replace(old_add, new_add)

# 4. Refactor end_level payout logic
old_end = """func end_level() -> void:
	is_in_level = false
	timer.stop()
	
	if current_gold >= target_quota:
		level_completed.emit()
		# Logic to move to shop/upgrade phase goes here
	else:
		game_over.emit()
		# Add meta progression resources here
		MetaProgression.add_meta_resource(floor(current_gold * 0.1))"""

new_end = """func end_level() -> void:
	is_in_level = false
	timer.stop()
	
	if current_score >= target_quota:
		_calculate_payout()
		level_completed.emit()
	else:
		game_over.emit()
		MetaProgression.add_meta_resource(floor(current_score * 0.05))

func _calculate_payout() -> void:
	var payout = 0
	# 1. Base Payout
	payout += 3
	
	# 2. Over-quota bonus (1 coin per 100 extra score)
	if current_score > target_quota:
		var extra = current_score - target_quota
		payout += floor(extra / 100)
		
	# 3. Interest (1 coin per 5 held, capped at interest_cap)
	var interest = min(floor(current_coins / 5), interest_cap)
	payout += interest
	
	add_coins(payout)
	print("Level cleared! Base: 3 | Bonus: %d | Interest: %d | Total Payout: %d" % [floor((current_score - target_quota)/100.0) if current_score>target_quota else 0, interest, payout])
"""

content = content.replace(old_end, new_end)

# Also fix the level transition to clear score
old_adv = """func advance_to_next_level() -> void:
	current_level += 1
	target_quota = _calculate_quota(current_level)
	level_changed.emit(current_level)
	quota_changed.emit(target_quota)"""

new_adv = """func advance_to_next_level() -> void:
	current_score = 0
	current_level += 1
	target_quota = _calculate_quota(current_level)
	score_changed.emit(current_score)
	level_changed.emit(current_level)
	quota_changed.emit(target_quota)"""

content = content.replace(old_adv, new_adv)


with open("scripts/singletons/GameManager.gd", "w") as f:
    f.write(content)
