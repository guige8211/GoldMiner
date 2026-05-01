import re

with open("scenes/Player.tscn", "r") as f:
    content = f.read()

# Original vertices were: -15, -10, 15, -10, 0, 20
# Let's check how Line2D looks. Line goes from (0,0) down to (0, 50).
# The 'Tip' Area2D is at (0, 50).
# If we put a Polygon2D inside Tip, (0,0) of Polygon2D is exactly at (0,50) of Hook.
# The Line2D touches (0,50). 
# A downward pointing triangle should have its top edge bisected by (0,0) or its tip at (0,0).
# Let's make the tip be at (0, 20) and the base be at (-15, 0) to (15, 0).
# This means the triangle is drawn completely below the line's end point.
# Let's try: base at (-15, -5), (15, -5), tip at (0, 15).

old_poly = "polygon = PackedVector2Array(-15, -10, 15, -10, 0, 20)"
new_poly = "polygon = PackedVector2Array(-12, -5, 12, -5, 0, 15)"

content = content.replace(old_poly, new_poly)

with open("scenes/Player.tscn", "w") as f:
    f.write(content)
