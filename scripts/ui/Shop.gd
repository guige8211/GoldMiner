extends Control
class_name Shop

@export var shop_item_scene: PackedScene

@onready var gold_label = $GoldLabel
@onready var items_container = $ItemsContainer

func _ready() -> void:
	_update_gold_display()
	_generate_shop_items()
	GameManager.coins_changed.connect(_on_coins_changed)
	_update_inventory()

func _update_gold_display() -> void:
	gold_label.text = "Coins: %d" % GameManager.current_coins

func _on_coins_changed(new_coins: int) -> void:
	_update_gold_display()
	# Update all buttons if they can still afford it
	for child in items_container.get_children():
		if child is ShopItem and not child.buy_button.text == "SOLD":
			child.update_button_state(new_coins)

func _generate_shop_items() -> void:
	# Clear container
	for child in items_container.get_children():
		child.queue_free()
		
	# Pick 3 random unique items from the ItemDB
	var random_items = ItemDB.get_random_upgrades(3, UpgradeManager.active_items)
	
	for i in range(random_items.size()):
		var item_data = random_items[i]
		var item_ui = shop_item_scene.instantiate() as ShopItem
		items_container.add_child(item_ui)
		item_ui.setup(item_data, GameManager.current_coins)
		item_ui.purchased.connect(_on_item_purchased)

func _on_item_purchased(item_data: Dictionary, shop_item_node: ShopItem) -> void:
	var price = item_data["price"]
	if GameManager.current_coins >= price:
		GameManager.add_coins(-price)
		
		# Apply the upgrade via UpgradeManager's new method
		UpgradeManager.add_upgrade(item_data["id"])
		_update_inventory()
		
		shop_item_node.mark_sold()

func _on_next_level_pressed() -> void:
	# We transition back to Level.tscn, and GameManager advances level
	GameManager.advance_to_next_level()
	get_tree().change_scene_to_file("res://scenes/Level.tscn")


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
		icon.tooltip_text = data.get("name", "") + "\n" + data.get("desc", "")
		grid.add_child(icon)
