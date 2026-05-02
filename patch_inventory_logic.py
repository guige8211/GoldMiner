with open("scripts/Level.gd", "r") as f:
    level_gd = f.read()

inventory_logic = """
	_update_inventory()

func _update_inventory() -> void:
	var grid = get_node_or_null("UI/InventoryPanel/ScrollContainer/InventoryGrid")
	if not grid: return
	
	for child in grid.get_children():
		child.queue_free()
		
	for item_id in UpgradeManager.active_items:
		var data = ItemDB.get_upgrade(item_id)
		if data.is_empty(): continue
		
		var icon = ColorRect.new()
		icon.custom_minimum_size = Vector2(60, 60)
		icon.color = data.get("color", Color.WHITE)
		icon.tooltip_text = data.get("name", "") + "\\n" + data.get("desc", "")
		grid.add_child(icon)
"""

level_gd = level_gd.replace("	GameManager.start_level()", "	GameManager.start_level()\n" + inventory_logic)

with open("scripts/Level.gd", "w") as f:
    f.write(level_gd)

with open("scripts/ui/Shop.gd", "r") as f:
    shop_gd = f.read()

shop_inv_logic = """
func _update_inventory() -> void:
	var grid = get_node_or_null("InventoryPanel/ScrollContainer/InventoryGrid")
	if not grid: return
	
	for child in grid.get_children():
		child.queue_free()
		
	for item_id in UpgradeManager.active_items:
		var data = ItemDB.get_upgrade(item_id)
		if data.is_empty(): continue
		
		var icon = ColorRect.new()
		icon.custom_minimum_size = Vector2(60, 60)
		icon.color = data.get("color", Color.WHITE)
		icon.tooltip_text = data.get("name", "") + "\\n" + data.get("desc", "")
		grid.add_child(icon)
"""

# Call it in _ready
shop_gd = shop_gd.replace("	GameManager.coins_changed.connect(_on_coins_changed)", "	GameManager.coins_changed.connect(_on_coins_changed)\n\t_update_inventory()")

# Also call it in _on_item_purchased
shop_gd = shop_gd.replace('UpgradeManager.add_upgrade(item_data["id"])', 'UpgradeManager.add_upgrade(item_data["id"])\n\t\t_update_inventory()')

# Append function
shop_gd += "\n" + shop_inv_logic

with open("scripts/ui/Shop.gd", "w") as f:
    f.write(shop_gd)
