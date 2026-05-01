extends Node2D

@onready var gold_label: Label = $UI/HUD/TopPanel/GoldLabel
@onready var quota_label: Label = $UI/HUD/TopPanel/QuotaLabel
@onready var time_label: Label = $UI/HUD/TopPanel/TimeLabel
@onready var level_label: Label = $UI/HUD/TopPanel/LevelLabel
@onready var message_label: Label = $UI/HUD/MessageLabel
@onready var level_generator: LevelGenerator = $LevelGenerator

func _ready() -> void:
	# Connect to GameManager signals
	if not GameManager.gold_changed.is_connected(_on_gold_changed):
		GameManager.gold_changed.connect(_on_gold_changed)
		GameManager.quota_changed.connect(_on_quota_changed)
		GameManager.timer_updated.connect(_on_timer_updated)
		GameManager.level_changed.connect(_on_level_changed)
		GameManager.level_completed.connect(_on_level_completed)
		GameManager.game_over.connect(_on_game_over)
	
	# If level is 1 and gold is 0, we assume it's a new run
	if GameManager.current_level == 1 and GameManager.current_gold == 0 and not GameManager.is_in_level:
		GameManager.start_new_run()
		
	# Trigger the UI update manually for when we return from shop
	_on_gold_changed(GameManager.current_gold)
	_on_quota_changed(GameManager.target_quota)
	_on_level_changed(GameManager.current_level)
	
	# Start the timer for this level
	GameManager.start_level()

func _on_gold_changed(new_gold: int) -> void:
	gold_label.text = "Gold: $%d" % new_gold

func _on_quota_changed(new_quota: int) -> void:
	quota_label.text = "Target: $%d" % new_quota

func _on_timer_updated(time_left: float) -> void:
	time_label.text = "Time: %d" % int(time_left)

func _on_level_changed(new_level: int) -> void:
	level_label.text = "Level %d" % new_level
	level_generator.generate_level(new_level, GameManager.target_quota)
	message_label.hide()

func _on_level_completed() -> void:
	message_label.text = "LEVEL COMPLETE!"
	message_label.add_theme_color_override("font_color", Color.GREEN)
	message_label.show()
	
	# In a real game, you would transition to the shop here
	# For prototype, we'll just wait 2 seconds and advance
	await get_tree().create_timer(2.0).timeout
	get_tree().change_scene_to_file("res://scenes/Shop.tscn")

func _on_game_over() -> void:
	message_label.text = "GAME OVER\nFAILED QUOTA"
	message_label.add_theme_color_override("font_color", Color.RED)
	message_label.show()
	
	# Wait and restart
	await get_tree().create_timer(3.0).timeout
	GameManager.start_new_run()
