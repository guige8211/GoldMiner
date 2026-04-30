extends Node

signal gold_changed(new_gold)
signal quota_changed(new_quota)
signal level_changed(new_level)
signal timer_updated(time_left)
signal game_over()
signal level_completed()

var current_gold: int = 0
var target_quota: int = 100
var current_level: int = 1
var time_left: float = 60.0
var is_in_level: bool = false

@onready var timer: Timer = Timer.new()

func _ready() -> void:
	add_child(timer)
	timer.wait_time = 1.0
	timer.timeout.connect(_on_timer_tick)
	
func start_new_run() -> void:
	current_gold = 0
	current_level = 1
	target_quota = _calculate_quota(current_level)
	gold_changed.emit(current_gold)
	quota_changed.emit(target_quota)
	level_changed.emit(current_level)
	start_level()

func start_level() -> void:
	time_left = 60.0 # Base time, can be modified by UpgradeManager later
	is_in_level = true
	timer.start()

func end_level() -> void:
	is_in_level = false
	timer.stop()
	
	if current_gold >= target_quota:
		level_completed.emit()
		# Logic to move to shop/upgrade phase goes here
	else:
		game_over.emit()
		# Add meta progression resources here
		MetaProgression.add_meta_resource(floor(current_gold * 0.1))

func advance_to_next_level() -> void:
	current_level += 1
	target_quota = _calculate_quota(current_level)
	level_changed.emit(current_level)
	quota_changed.emit(target_quota)
	start_level()

func add_gold(amount: int) -> void:
	current_gold += amount
	gold_changed.emit(current_gold)

func _on_timer_tick() -> void:
	if is_in_level:
		time_left -= 1.0
		timer_updated.emit(time_left)
		if time_left <= 0:
			end_level()

func _calculate_quota(level: int) -> int:
	# A simple exponential/linear curve for testing
	return int(100 * level + pow(level, 1.5) * 50)
