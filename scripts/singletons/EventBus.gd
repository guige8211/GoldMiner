extends Node

# Centralized Event Bus for decoupling gameplay systems from upgrades

# Fired when the hook is thrown
signal hook_fired()

# Fired the exact moment the hook touches an item
signal item_grabbed(item: Node2D)

# Fired when the item successfully returns to the player
signal item_collected(item: Node2D)

# Signal used to allow Upgrades to intercept and modify values dynamically.
# GDScript doesn't have reference passing for simple types easily through signals,
# so we pass a dictionary context that observers can modify.
signal request_item_value_modifiers(item: Node2D, context: Dictionary)
signal request_retract_speed_modifiers(item: Node2D, context: Dictionary)
