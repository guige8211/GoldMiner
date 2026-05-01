extends Node2D
class_name Player

@onready var hook = $Hook

func _ready() -> void:
	if not hook:
		push_warning("Player is missing a Hook node.")

func _process(delta: float) -> void:
	# Only process input if we are in a level and the hook is idling/swinging
	if not GameManager.is_in_level:
		return
		
	if Input.is_action_just_pressed("ui_accept") or Input.is_key_pressed(KEY_SPACE) or Input.is_key_pressed(KEY_DOWN):
		if hook.current_state == hook.HookState.SWINGING:
			hook.fire()
