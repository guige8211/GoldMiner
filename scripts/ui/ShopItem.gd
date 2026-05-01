extends Panel
class_name ShopItem

signal purchased(item_data, node)

@onready var name_label = $VBoxContainer/NameLabel
@onready var desc_label = $VBoxContainer/DescLabel
@onready var price_label = $VBoxContainer/PriceLabel
@onready var buy_button = $VBoxContainer/BuyButton
@onready var icon_rect = $VBoxContainer/IconRect

var item_data: Dictionary = {}

func setup(data: Dictionary, current_gold: int) -> void:
	item_data = data
	name_label.text = data.get("name", "Unknown")
	desc_label.text = data.get("desc", "No description.")
	price_label.text = "$%d" % data.get("price", 999)
	
	if data.has("color"):
		icon_rect.color = data["color"]
		
	update_button_state(current_gold)

func update_button_state(current_gold: int) -> void:
	if item_data.is_empty():
		return
		
	if current_gold >= item_data.get("price", 999):
		buy_button.disabled = false
		buy_button.text = "BUY"
	else:
		buy_button.disabled = true
		buy_button.text = "NOT ENOUGH"

func _on_buy_button_pressed() -> void:
	purchased.emit(item_data, self)
	
func mark_sold() -> void:
	buy_button.disabled = true
	buy_button.text = "SOLD"
	modulate = Color(0.5, 0.5, 0.5, 1) # Dim the item
