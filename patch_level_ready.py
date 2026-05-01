with open("scripts/Level.gd", "r") as f:
    content = f.read()

old_ready = """func _ready() -> void:
	# Connect to GameManager signals
	GameManager.gold_changed.connect(_on_gold_changed)
	GameManager.quota_changed.connect(_on_quota_changed)
	GameManager.timer_updated.connect(_on_timer_updated)
	GameManager.level_changed.connect(_on_level_changed)
	GameManager.level_completed.connect(_on_level_completed)
	GameManager.game_over.connect(_on_game_over)
	
	# Start the first run
	GameManager.start_new_run()"""

new_ready = """func _ready() -> void:
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
	GameManager.start_level()"""

content = content.replace(old_ready, new_ready)

with open("scripts/Level.gd", "w") as f:
    f.write(content)
