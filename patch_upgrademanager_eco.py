with open("scripts/singletons/UpgradeManager.gd", "r") as f:
    content = f.read()

# Make sure UpgradeManager hooks into EventBus.item_collected to handle gold_rush
old_collect = """	# Pocket Watch Logic
	if has_upgrade("pocket_watch"):
		GameManager.time_left += 2.0
		# Clamp or just let it exceed base time? Let's let it exceed.
		GameManager.timer_updated.emit(GameManager.time_left)"""

new_collect = """	# Pocket Watch Logic
	if has_upgrade("pocket_watch"):
		GameManager.time_left += 2.0
		# Clamp or just let it exceed base time? Let's let it exceed.
		GameManager.timer_updated.emit(GameManager.time_left)
		
	# Gold Rush Logic
	if has_upgrade("gold_rush") and item.item_name == "Small Gold":
		GameManager.add_coins(1)"""

content = content.replace(old_collect, new_collect)

# Add Greedy Pot logic (modifying GameManager.interest_cap when added)
old_add = """	# Apply static stats immediately
	if data.get("type") == "static":
		var stat = data.get("stat")
		var val = data.get("value")
		if stat and val != null:
			set(stat, get(stat) + val)"""

new_add = """	# Apply static stats immediately
	if data.get("type") == "static":
		var stat = data.get("stat")
		var val = data.get("value")
		if stat and val != null:
			set(stat, get(stat) + val)
			
	# Greedy Pot one-time activation
	if id == "greedy_pot":
		GameManager.interest_cap = 15"""

content = content.replace(old_add, new_add)

# Add Appraisal logic
old_val = """	# Geologist Logic
	if has_upgrade("geologist") and item.get("type") == 1: # 1 is ROCK
		context["base_value"] = 80 # Override base value completely"""

new_val = """	# Geologist Logic
	if has_upgrade("geologist") and item.get("type") == 1: # 1 is ROCK
		context["base_value"] = 80 # Override base value completely
		
	# Appraisal Logic
	if has_upgrade("appraisal"):
		context["base_value"] += 30"""

content = content.replace(old_val, new_val)

with open("scripts/singletons/UpgradeManager.gd", "w") as f:
    f.write(content)
