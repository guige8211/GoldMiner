with open("scripts/player/Hook.gd", "r") as f:
    content = f.read()

# I previously wrote:
# var dir = Vector2.DOWN
# var tip_pos = dir * (50.0 + current_length)
# But wait, Hook is rotating, so Vector2.DOWN * length is correct for local space if Hook is Node2D.
# Why did it look crooked in the screenshot? 
# Ah! In the user's screenshot, there is no triangle, there is a magenta box.
# Wait, did my triangle push (which happened 5 pushes ago) not get fetched properly by the player?
# Or maybe the AimLine starts at (0,50) but Hook origin is (0,32) and rotation pivots from (0,0).
# Let's fix AimLine completely by redrawing it dynamically from (0,50) to (0,800) in local space,
# BUT we will explicitly enforce points in _process.

old_update = """	var line_node = get_node_or_null("Line2D")
	if line_node:
		line_node.points = [Vector2.ZERO, tip_pos]
		
	# Keep AimLine pointing correctly regardless of length
	var aim_line = get_node_or_null("AimLine")
	if aim_line and current_state == HookState.SWINGING:
		aim_line.points = [Vector2.ZERO, dir * 800.0]"""

new_update = """	var line_node = get_node_or_null("Line2D")
	if line_node:
		line_node.points = [Vector2.ZERO, tip_pos]
		
	# Fix AimLine offset: The rope starts at (0,0), tip defaults at (0,50). 
	# The AimLine should start exactly where the tip is and point downwards.
	var aim_line = get_node_or_null("AimLine")
	if aim_line and current_state == HookState.SWINGING:
		aim_line.points = [tip_pos, Vector2.DOWN * 1200.0]"""

content = content.replace(old_update, new_update)

with open("scripts/player/Hook.gd", "w") as f:
    f.write(content)
