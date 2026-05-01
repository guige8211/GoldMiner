with open("scripts/singletons/GameManager.gd", "r") as f:
    content = f.read()

# Make sure we don't duplicate logic. Since Shop.gd calls advance_to_next_level() and then changes scene,
# we need to make sure start_level() doesn't do anything weird to the tree. 
# It currently just sets time_left and starts timer, which is fine, but timer shouldn't tick if we aren't in Level.tscn.
# Actually, the way it's set up, is_in_level becomes true, but the Shop scene has no timer display.
# It's better to NOT call start_level() in advance_to_next_level() and instead call start_level() in Level.gd's _ready.

old_code = """func advance_to_next_level() -> void:
	current_level += 1
	target_quota = _calculate_quota(current_level)
	level_changed.emit(current_level)
	quota_changed.emit(target_quota)
	start_level()"""

new_code = """func advance_to_next_level() -> void:
	current_level += 1
	target_quota = _calculate_quota(current_level)
	level_changed.emit(current_level)
	quota_changed.emit(target_quota)
	# start_level will be called by Level.gd when it loads"""

content = content.replace(old_code, new_code)

old_start = """func start_new_run() -> void:
	current_gold = 0
	current_level = 1
	target_quota = _calculate_quota(current_level)
	gold_changed.emit(current_gold)
	quota_changed.emit(target_quota)
	level_changed.emit(current_level)
	start_level()"""

new_start = """func start_new_run() -> void:
	UpgradeManager.reset_run()
	current_gold = 0
	current_level = 1
	target_quota = _calculate_quota(current_level)
	gold_changed.emit(current_gold)
	quota_changed.emit(target_quota)
	level_changed.emit(current_level)
	# start_level will be called by Level.gd"""

content = content.replace(old_start, new_start)

with open("scripts/singletons/GameManager.gd", "w") as f:
    f.write(content)
