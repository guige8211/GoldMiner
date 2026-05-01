import re

with open("scenes/Player.tscn", "r") as f:
    content = f.read()

# Remove the old ColorRect which was the grey square
old_rect = """[node name="ClawVisual" type="ColorRect" parent="Hook/Tip"]
offset_left = -10.0
offset_top = -10.0
offset_right = 10.0
offset_bottom = 10.0
color = Color(0.752941, 0.752941, 0.752941, 1)"""

# Add a Polygon2D which forms a downward pointing triangle (looks like a claw or arrow)
# Vertices: (-15, -10), (15, -10), (0, 20) -> Pointing down
new_polygon = """[node name="ClawVisual" type="Polygon2D" parent="Hook/Tip"]
color = Color(0.8, 0.8, 0.8, 1)
polygon = PackedVector2Array(-15, -10, 15, -10, 0, 20)"""

content = content.replace(old_rect, new_polygon)

with open("scenes/Player.tscn", "w") as f:
    f.write(content)
