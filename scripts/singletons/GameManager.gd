extends Node

signal score_changed(new_score)
signal coins_changed(new_coins)
signal quota_changed(new_quota)
signal level_changed(new_level)
signal timer_updated(time_left)
signal game_over()
signal level_completed()

var current_score: int = 0
var current_coins: int = 0
var interest_cap: int = 5
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
	UpgradeManager.reset_run()
	current_score = 0
	current_coins = 3
	interest_cap = 5
	current_level = 1
	target_quota = _calculate_quota(current_level)
	score_changed.emit(current_score)
	coins_changed.emit(current_coins)
	quota_changed.emit(target_quota)
	level_changed.emit(current_level)
	# start_level will be called by Level.gd

func start_level() -> void:
	time_left = 60.0 # Base time, can be modified by UpgradeManager later
	is_in_level = true
	timer.start()

func end_level() -> void:
	is_in_level = false
	timer.stop()
	
	if current_score >= target_quota:
		_calculate_payout()
		level_completed.emit()
	else:
		game_over.emit()
		MetaProgression.add_meta_resource(floor(current_score * 0.05))

func _calculate_payout() -> void:
	var payout = 0
	# 1. Base Payout scales with level
	var base_pay = 3 + current_level
	payout += base_pay
	
	# 2. Over-quota bonus (1 coin per 30 extra score)
	if current_score > target_quota:
		var extra = current_score - target_quota
		payout += floor(extra / 30.0)
		
	# 3. Interest (1 coin per 5 held, capped at interest_cap)
	var interest = 0
	if UpgradeManager.has_upgrade("compound_interest"):
		interest = floor(current_coins * 0.1) # 10% of total wealth, NO CAP!
	else:
		interest = min(floor(current_coins / 5), interest_cap)
	payout += interest
	
	add_coins(payout)
	print("Level cleared! Base: 3 | Bonus: %d | Interest: %d | Total Payout: %d" % [floor((current_score - target_quota)/50.0) if current_score>target_quota else 0, interest, payout])


func advance_to_next_level() -> void:
	current_score = 0
	current_level += 1
	target_quota = _calculate_quota(current_level)
	score_changed.emit(current_score)
	level_changed.emit(current_level)
	quota_changed.emit(target_quota)
	# start_level will be called by Level.gd when it loads

func add_score(amount: int) -> void:
	current_score += amount
	score_changed.emit(current_score)

func add_coins(amount: int) -> void:
	current_coins += amount
	coins_changed.emit(current_coins)

func _on_timer_tick() -> void:
	if is_in_level:
		time_left -= 1.0
		timer_updated.emit(time_left)
		if time_left <= 0:
			end_level()

func _calculate_quota(level: int) -> int:
	# A simple exponential/linear curve for testing
	return 100 + (level - 1) * 150
