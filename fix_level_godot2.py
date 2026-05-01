with open("scripts/Level.gd", "r") as f:
    content = f.read()

# I see it now.
# `GameManager.start_new_run()` calls `level_changed.emit(current_level)`.
# `Level.gd` connects `level_changed` to `_on_level_changed`.
# So when `start_new_run()` fires, it calls `level_generator.generate_level(new_level, GameManager.target_quota)`.
#
# THEN, right after `GameManager.start_new_run()`, `Level.gd` manually calls `_on_level_changed(GameManager.current_level)` AGAIN.
# This causes `level_generator.generate_level` to fire a SECOND time immediately.
# `generate_level` starts by calling `queue_free()` on all children of ItemsRoot.
# Since `queue_free()` is deferred to the end of the frame, the FIRST batch of items are marked for deletion.
# The SECOND batch of items are created.
# Wait, if both happen in the same frame, maybe the first batch clears the second?
# Actually, `queue_free` clears them all.

old_ready = """	# Trigger the UI update manually for when we return from shop
	_on_score_changed(GameManager.current_score)
	_on_coins_changed(GameManager.current_coins)
	_on_quota_changed(GameManager.target_quota)
	_on_level_changed(GameManager.current_level)"""

new_ready = """	# Trigger the UI update manually for when we return from shop
	_on_score_changed(GameManager.current_score)
	_on_coins_changed(GameManager.current_coins)
	_on_quota_changed(GameManager.target_quota)
	
	# Only manually trigger level generation if we didn't just start a new run
	if GameManager.current_level > 1 or GameManager.current_score > 0:
		_on_level_changed(GameManager.current_level)"""

content = content.replace(old_ready, new_ready)

with open("scripts/Level.gd", "w") as f:
    f.write(content)
