import re

with open("scenes/Player.tscn", "r") as f:
    content = f.read()

# Add AimLine to the Hook node.
# The Hook rotates, so a Line2D placed as a direct child of Hook will rotate with it.
# We draw it starting from the origin (0, 0) and extending deeply down (0, 800).
# Since Godot 4 Line2D doesn't have an explicit 'dashed' property without custom shaders/textures in tscn easily,
# we will use a solid thin white line with low alpha (opacity) to represent the laser sight.

aim_line_node = """[node name="AimLine" type="Line2D" parent="Hook"]
points = PackedVector2Array(0, 50, 0, 800)
width = 2.0
default_color = Color(1, 1, 1, 0.25)
"""

# Insert it inside Hook, right before Line2D (the rope)
content = content.replace('[node name="Line2D" type="Line2D" parent="Hook"]', aim_line_node + '\n[node name="Line2D" type="Line2D" parent="Hook"]')

with open("scenes/Player.tscn", "w") as f:
    f.write(content)
