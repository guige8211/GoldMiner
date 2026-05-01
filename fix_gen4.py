with open("scripts/systems/LevelGenerator.gd", "r") as f:
    content = f.read()

# I see the problem. The spawn positions are probably off-screen because
# of my fallback logic in _find_valid_position, OR they are spawning properly but invisible
# due to some visibility flag.
# But wait! In the screenshot from earlier (BLH66Rp.png) BEFORE I "fixed" the uid error,
# there WERE rocks and gold chunks visible!
# Look at my log from when I restored the files:
# LOG: Spawns: { "gold_small": 2, "gold_large": 1, "diamond": 0, "rock": 5 }
# They ARE spawning. Why are they not visible?
# Because in `scenes/items/GoldSmall.tscn` etc, I might have messed up the `Sprite2D` node!
# No, I used `PlaceholderTexture2D`. But wait, maybe `PlaceholderTexture2D` isn't supported properly
# in exported HTML5 builds unless they are explicitly created or sized?
# Or maybe because I didn't include the resources in the export filter?
# No, `export_filter="all_resources"`.
# Let's replace PlaceholderTexture2D with simple ColorRects just to be absolutely certain they render.

import os

for item in ["GoldSmall", "GoldLarge", "Rock", "Diamond"]:
    filepath = f"scenes/items/{item}.tscn"
    with open(filepath, "r") as f:
        file_content = f.read()
    
    # Remove the PlaceholderTexture2D stuff
    file_content = file_content.replace('[sub_resource type="PlaceholderTexture2D" id="PlaceholderTexture2D_item"]\n', '')
    import re
    file_content = re.sub(r'size = Vector2\([0-9]+, [0-9]+\)\n', '', file_content, count=1)
    
    # Replace Sprite2D with ColorRect
    color_map = {
        "GoldSmall": "Color(1, 0.843137, 0, 1)",
        "GoldLarge": "Color(1, 0.74902, 0, 1)",
        "Rock": "Color(0.411765, 0.411765, 0.411765, 1)",
        "Diamond": "Color(0, 0.866667, 1, 1)"
    }
    size_map = {
        "GoldSmall": "25.0",
        "GoldLarge": "60.0",
        "Rock": "45.0",
        "Diamond": "15.0"
    }
    
    color_rect_node = f"""[node name="ColorRect" type="ColorRect" parent="."]
offset_left = -{float(size_map[item])/2}
offset_top = -{float(size_map[item])/2}
offset_right = {float(size_map[item])/2}
offset_bottom = {float(size_map[item])/2}
color = {color_map[item]}"""

    file_content = re.sub(r'\[node name="Sprite2D".*?texture = SubResource\("PlaceholderTexture2D_item"\)', color_rect_node, file_content, flags=re.DOTALL)
    
    with open(filepath, "w") as f:
        f.write(file_content)

