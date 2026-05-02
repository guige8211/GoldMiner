with open("scripts/player/Hook.gd", "r") as f:
    content = f.read()

# I see what went wrong. In _update_hook_position:
# var dir = Vector2.DOWN.rotated(rotation)
# This is WRONG!
# The Hook node ITSELF is rotating via `rotation_degrees += ...`
# So Vector2.DOWN is ALREADY rotated by the parent node!
# If you rotate it AGAIN inside the script, you are double-rotating the positions,
# which causes the physics/Tip Area2D to swing twice as fast and completely misalign from the AimLine 
# (because AimLine is just a child of Hook, so it naturally rotates once).

old_pos = """	var dir = Vector2.DOWN.rotated(rotation)
	var tip_pos = dir * current_length"""

new_pos = """	# Hook node itself rotates, so local downward direction is always just Vector2.DOWN
	var dir = Vector2.DOWN
	# The base length of the rope starts at 50 (from 0,0 to 0,50 where Tip sits initially)
	var tip_pos = dir * (50.0 + current_length)"""

content = content.replace(old_pos, new_pos)

# Also fix the initial AimLine visibility and Line2D update logic
old_line = """	var line_node = get_node_or_null("Line2D")
	if line_node:
		line_node.points = [Vector2.ZERO, tip_pos]"""

new_line = """	var line_node = get_node_or_null("Line2D")
	if line_node:
		line_node.points = [Vector2.ZERO, tip_pos]
		
	# Keep AimLine pointing correctly regardless of length
	var aim_line = get_node_or_null("AimLine")
	if aim_line and current_state == HookState.SWINGING:
		aim_line.points = [Vector2.ZERO, dir * 800.0]"""

content = content.replace(old_line, new_line)

with open("scripts/player/Hook.gd", "w") as f:
    f.write(content)
