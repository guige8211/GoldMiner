with open("scripts/ui/Shop.gd", "r") as f:
    content = f.read()

content = content.replace("GameManager.gold_changed.connect(_on_gold_changed)", "GameManager.coins_changed.connect(_on_coins_changed)")

old_upd = """func _update_gold_display() -> void:
	gold_label.text = "Gold: $%d" % GameManager.current_gold

func _on_gold_changed(new_gold: int) -> void:
	_update_gold_display()
	# Update all buttons if they can still afford it
	for child in items_container.get_children():
		if child is ShopItem and not child.buy_button.text == "SOLD":
			child.update_button_state(new_gold)"""

new_upd = """func _update_gold_display() -> void:
	gold_label.text = "Coins: %d" % GameManager.current_coins

func _on_coins_changed(new_coins: int) -> void:
	_update_gold_display()
	# Update all buttons if they can still afford it
	for child in items_container.get_children():
		if child is ShopItem and not child.buy_button.text == "SOLD":
			child.update_button_state(new_coins)"""

content = content.replace(old_upd, new_upd)
content = content.replace("GameManager.current_gold", "GameManager.current_coins")
content = content.replace("GameManager.add_gold(-price)", "GameManager.add_coins(-price)")

with open("scripts/ui/Shop.gd", "w") as f:
    f.write(content)

with open("scripts/ui/ShopItem.gd", "r") as f:
    content = f.read()
content = content.replace('price_label.text = "$%d" % data.get("price", 999)', 'price_label.text = "Cost: %d" % data.get("price", 99)')
with open("scripts/ui/ShopItem.gd", "w") as f:
    f.write(content)
