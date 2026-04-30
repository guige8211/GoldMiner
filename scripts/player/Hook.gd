extends Node2D
class_name Hook

enum HookState { SWINGING, EXTENDING, RETRACTING }

@export var max_swing_angle: float = 75.0 # Degrees
@export var swing_speed: float = 60.0 # Degrees per second
@export var extend_speed: float = 400.0 # Pixels per second
@export var base_retract_speed: float = 400.0 # Pixels per second
@export var max_length: float = 600.0

var current_state: HookState = HookState.SWINGING
var swing_direction: int = 1
var current_length: float = 0.0
var grabbed_item: Node2D = null

@onready var origin_point: Vector2 = position

func _ready() -> void:
	rotation_degrees = -max_swing_angle

func _process(delta: float) -> void:
	match current_state:
		HookState.SWINGING:
			_process_swing(delta)
		HookState.EXTENDING:
			_process_extend(delta)
		HookState.RETRACTING:
			_process_retract(delta)

func _process_swing(delta: float) -> void:
	# Modulate swing speed based on upgrades if needed
	var actual_swing_speed = swing_speed * UpgradeManager.hook_speed_multiplier
	rotation_degrees += swing_direction * actual_swing_speed * delta
	
	if rotation_degrees >= max_swing_angle:
		rotation_degrees = max_swing_angle
		swing_direction = -1
	elif rotation_degrees <= -max_swing_angle:
		rotation_degrees = -max_swing_angle
		swing_direction = 1

func _process_extend(delta: float) -> void:
	var actual_extend_speed = extend_speed * UpgradeManager.hook_extend_speed_multiplier
	current_length += actual_extend_speed * delta
	_update_hook_position()
	
	# Check max distance
	if current_length >= max_length:
		_start_retracting()

func _process_retract(delta: float) -> void:
	var retract_speed_modifier = 1.0
	if grabbed_item and grabbed_item.has_method("get_weight"):
		# Heavy items slow down retract speed
		retract_speed_modifier = max(0.1, 1.0 - (grabbed_item.get_weight() * 0.1))
	
	# Apply global upgrade multipliers
	retract_speed_modifier *= UpgradeManager.hook_speed_multiplier
	
	current_length -= base_retract_speed * retract_speed_modifier * delta
	_update_hook_position()
	
	if current_length <= 0:
		current_length = 0
		_on_retract_finished()

func _update_hook_position() -> void:
	# Calculate the tip position based on current angle and length
	# In a real setup, you'd move the tip CharacterBody2D or Area2D
	# and draw a Line2D from origin to tip.
	var dir = Vector2.DOWN.rotated(rotation)
	var tip_pos = dir * current_length
	
	# Assuming there's a child node called "Tip" that has the Area2D
	var tip_node = get_node_or_null("Tip")
	if tip_node:
		tip_node.position = tip_pos
		
	# Update Line2D
	var line_node = get_node_or_null("Line2D")
	if line_node:
		line_node.points = [Vector2.ZERO, tip_pos]

func fire() -> void:
	if current_state == HookState.SWINGING:
		current_state = HookState.EXTENDING

func _start_retracting() -> void:
	current_state = HookState.RETRACTING

func _on_retract_finished() -> void:
	if grabbed_item:
		# Process the item
		if grabbed_item.has_method("collect"):
			grabbed_item.collect()
		grabbed_item.queue_free()
		grabbed_item = null
	
	current_state = HookState.SWINGING
	_update_hook_position()

# This should be connected to the Area2D's body_entered or area_entered signal on the Tip
func _on_tip_area_entered(area: Area2D) -> void:
	if current_state == HookState.EXTENDING and grabbed_item == null:
		if area.is_in_group("grabbable"):
			grab_item(area)

func grab_item(item: Node2D) -> void:
	grabbed_item = item
	# Disable the item's own collision so it doesn't interact with others while being pulled
	if item is Area2D:
		item.set_deferred("monitoring", false)
		item.set_deferred("monitorable", false)
	
	# Reparent the item to the tip so it follows the hook
	var tip_node = get_node_or_null("Tip")
	if tip_node:
		var global_pos = item.global_position
		item.get_parent().remove_child(item)
		tip_node.add_child(item)
		# Animate moving item to exact tip center if needed
		item.position = Vector2.ZERO
		
	_start_retracting()
