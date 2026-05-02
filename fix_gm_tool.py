with open("scripts/items/ItemBase.gd", "r") as f:
    content = f.read()

# Ah! Look at `ItemBase.gd`. The `collect()` function is still using the old implementation
# that calls `GameManager.add_gold(base_value)` and uses the old multipliers.
# BUT WAIT. Didn't I run `patch_item_base.py` to rewrite this to use the `EventBus.request_item_value_modifiers`?!
# Yes, but it got reverted during one of my forced rebase conflicts or when I recreated the files.
# AND it also calls `GameManager.add_gold`, which doesn't exist anymore! It's `add_score` and `add_coins`.
# No wonder `K` breaks the game. When `collect()` is called, it tries to call a missing method and the script crashes quietly!

new_collect = """func collect() -> void:
	var context = {
		"base_value": base_value,
		"multiplier": 1.0
	}
	
	# Allow upgrades to modify context via EventBus
	EventBus.request_item_value_modifiers.emit(self, context)
	
	var final_value = int(context["base_value"] * context["multiplier"])
	
	if final_value > 0:
		GameManager.add_score(final_value)
		
	# Notify systems that an item was successfully collected
	EventBus.item_collected.emit(self)"""

import re
content = re.sub(r'func collect\(\) -> void:.*', new_collect, content, flags=re.DOTALL)

with open("scripts/items/ItemBase.gd", "w") as f:
    f.write(content)
