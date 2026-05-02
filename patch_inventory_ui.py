import re

# We need to add the Inventory UI to Level.tscn
with open("scenes/Level.tscn", "r") as f:
    level = f.read()

inventory_node = """
[node name="InventoryPanel" type="PanelContainer" parent="UI"]
anchors_preset = 4
anchor_top = 0.5
anchor_bottom = 0.5
offset_left = 20.0
offset_top = -200.0
offset_right = 100.0
offset_bottom = 200.0
grow_vertical = 2

[node name="ScrollContainer" type="ScrollContainer" parent="UI/InventoryPanel"]
layout_mode = 2
horizontal_scroll_mode = 0

[node name="InventoryGrid" type="GridContainer" parent="UI/InventoryPanel/ScrollContainer"]
layout_mode = 2
columns = 1
theme_override_constants/h_separation = 10
theme_override_constants/v_separation = 10
"""

level = level.replace('[node name="Environment" type="Node2D" parent="."]', inventory_node + '\n[node name="Environment" type="Node2D" parent="."]')

with open("scenes/Level.tscn", "w") as f:
    f.write(level)


# We need to add the Inventory UI to Shop.tscn as well
with open("scenes/Shop.tscn", "r") as f:
    shop = f.read()

shop_inventory = """
[node name="InventoryPanel" type="PanelContainer" parent="."]
layout_mode = 1
anchors_preset = 4
anchor_top = 0.5
anchor_bottom = 0.5
offset_left = 20.0
offset_top = -200.0
offset_right = 100.0
offset_bottom = 200.0
grow_vertical = 2

[node name="ScrollContainer" type="ScrollContainer" parent="InventoryPanel"]
layout_mode = 2
horizontal_scroll_mode = 0

[node name="InventoryGrid" type="GridContainer" parent="InventoryPanel/ScrollContainer"]
layout_mode = 2
columns = 1
theme_override_constants/h_separation = 10
theme_override_constants/v_separation = 10
"""

shop = shop.replace('[node name="ItemsContainer" type="HBoxContainer" parent="."]', shop_inventory + '\n[node name="ItemsContainer" type="HBoxContainer" parent="."]')

with open("scenes/Shop.tscn", "w") as f:
    f.write(shop)
