extends Control
class_name Shop

@export var shop_item_scene: PackedScene

@onready var gold_label = $GoldLabel
@onready var items_container = $ItemsContainer

# The pool of possible upgrades
var upgrade_pool = [
	{
		"id": "speed",
		"name": "Oil Can",
		"desc": "Increases hook swing and pull speed by 20%.",
		"price": 100,
		"stat": "hook_speed_multiplier",
		"value": 0.2,
		"color": Color.GRAY
	},
	{
		"id": "gold_value",
		"name": "Gold Polish",
		"desc": "Increases the value of all Gold by 25%.",
		"price": 150,
		"stat": "gold_value_multiplier",
		"value": 0.25,
		"color": Color.GOLD
	},
	{
		"id": "rock_value",
		"name": "Rock Collector Book",
		"desc": "Rocks are now worth 5x more money.",
		"price": 80,
		"stat": "rock_value_multiplier",
		"value": 4.0, # base is 1.0, +4.0 makes it 5.0
		"color": Color.DARK_GRAY
	},
	{
		"id": "diamond_chance",
		"name": "Lucky Clover",
		"desc": "Increases the chance of Diamonds spawning.",
		"price": 250,
		"stat": "diamond_spawn_chance_bonus",
		"value": 0.15,
		"color": Color.GREEN
	}
]

func _ready() -> void:
	_update_gold_display()
	_generate_shop_items()
	GameManager.coins_changed.connect(_on_coins_changed)

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
		
	# Pick 3 random unique items from the pool
	var pool_copy = upgrade_pool.duplicate()
	pool_copy.shuffle()
	
	for i in range(min(3, pool_copy.size())):
		var item_data = pool_copy[i]
		var item_ui = shop_item_scene.instantiate() as ShopItem
		items_container.add_child(item_ui)
		item_ui.setup(item_data, GameManager.current_coins)
		item_ui.purchased.connect(_on_item_purchased)

func _on_item_purchased(item_data: Dictionary, shop_item_node: ShopItem) -> void:
	var price = item_data["price"]
	if GameManager.current_coins >= price:
		GameManager.add_coins(-price)
		
		# Apply the upgrade via UpgradeManager
		var upgrade_to_apply = {
			"name": item_data["name"],
			"stat": item_data["stat"],
			"value": item_data["value"]
		}
		UpgradeManager._apply_item(upgrade_to_apply)
		
		shop_item_node.mark_sold()

func _on_next_level_pressed() -> void:
	# We transition back to Level.tscn, and GameManager advances level
	GameManager.advance_to_next_level()
	get_tree().change_scene_to_file("res://scenes/Level.tscn")
