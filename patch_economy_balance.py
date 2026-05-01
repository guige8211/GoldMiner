import re

with open("scripts/singletons/GameManager.gd", "r") as f:
    content = f.read()

# Fix initial coins
content = content.replace("current_coins = 0", "current_coins = 3")

# Fix payout formula
old_payout = """	# 2. Over-quota bonus (1 coin per 100 extra score)
	if current_score > target_quota:
		var extra = current_score - target_quota
		payout += floor(extra / 100.0)"""

new_payout = """	# 2. Over-quota bonus (1 coin per 50 extra score)
	if current_score > target_quota:
		var extra = current_score - target_quota
		payout += floor(extra / 50.0)"""

content = content.replace(old_payout, new_payout)

# Fix print statement text
content = content.replace("floor((current_score - target_quota)/100.0)", "floor((current_score - target_quota)/50.0)")

with open("scripts/singletons/GameManager.gd", "w") as f:
    f.write(content)
