extends Area2D
class_name ItemBase

enum ItemType { GOLD, ROCK, DIAMOND, CHEST, MYSTERY }

@export var item_name: String = "Unknown Item"
@export var type: ItemType = ItemType.GOLD
@export var base_value: int = 10
@export var weight: float = 1.0 # 1.0 is standard, higher means slower pull

func _ready() -> void:
	add_to_group("grabbable")

func get_weight() -> float:
	return weight

func collect() -> void:
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
