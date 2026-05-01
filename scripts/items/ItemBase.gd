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
	match type:
		ItemType.GOLD:
			var final_value = int(base_value * UpgradeManager.gold_value_multiplier)
			GameManager.add_score(final_value)
		ItemType.ROCK:
			var final_value = int(base_value * UpgradeManager.rock_value_multiplier)
			GameManager.add_score(final_value)
		ItemType.DIAMOND:
			GameManager.add_gold(base_value)
		ItemType.CHEST:
			UpgradeManager.add_pending_chest()
			# Maybe add a small base value for opening a chest too
			GameManager.add_gold(base_value)
		ItemType.MYSTERY:
			# Implement mystery logic (random gold, bomb, etc)
			pass
	
	# Play particle effects / sound here
