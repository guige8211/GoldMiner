with open("scripts/singletons/GameManager.gd", "r") as f:
    content = f.read()

# Modify payout logic to respect Compound Interest
old_interest = """	# 3. Interest (1 coin per 5 held, capped at interest_cap)
	var interest = min(floor(current_coins / 5), interest_cap)
	payout += interest"""

new_interest = """	# 3. Interest (1 coin per 5 held, capped at interest_cap)
	var interest = 0
	if UpgradeManager.has_upgrade("compound_interest"):
		interest = floor(current_coins * 0.1) # 10% of total wealth, NO CAP!
	else:
		interest = min(floor(current_coins / 5), interest_cap)
	payout += interest"""

content = content.replace(old_interest, new_interest)

with open("scripts/singletons/GameManager.gd", "w") as f:
    f.write(content)
