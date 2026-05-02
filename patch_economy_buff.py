with open("scripts/singletons/GameManager.gd", "r") as f:
    content = f.read()

# 1. Update initial coins to 5
content = content.replace("current_coins = 0\n\tinterest_cap = 5", "current_coins = 5\n\tinterest_cap = 5")

# 2. Update payout formula
old_payout = """func _calculate_payout() -> void:
	var payout = 0
	# 1. Base Payout
	payout += 3
	
	# 2. Over-quota bonus (1 coin per 100 extra score)
	if current_score > target_quota:
		var extra = current_score - target_quota
		payout += floor(extra / 100)"""

# Wait, my previous patch in step "Rebalance Payout Formula" failed to update the actual logic correctly
# in GameManager.gd due to my complete rewrite in "fix_gm.py" which overrode it with the original /100 logic.
# Let's fix this completely and robustly now.

new_payout = """func _calculate_payout() -> void:
	var payout = 0
	# 1. Base Payout scales with level
	var base_pay = 3 + current_level
	payout += base_pay
	
	# 2. Over-quota bonus (1 coin per 30 extra score)
	if current_score > target_quota:
		var extra = current_score - target_quota
		payout += floor(extra / 30.0)"""

import re
content = re.sub(r'func _calculate_payout\(\) -> void:.*?payout \+= floor\(extra / 100\)', new_payout, content, flags=re.DOTALL)

# Fix the print statement
old_print = """	print("Level cleared! Base: 3 | Bonus: %d | Interest: %d | Total Payout: %d" % [floor((current_score - target_quota)/100.0) if current_score>target_quota else 0, interest, payout])"""
new_print = """	print("Level cleared! Base: %d | Bonus: %d | Interest: %d | Total Payout: %d" % [base_pay, floor((current_score - target_quota)/30.0) if current_score>target_quota else 0, interest, payout])"""
content = content.replace(old_print, new_print)

with open("scripts/singletons/GameManager.gd", "w") as f:
    f.write(content)
