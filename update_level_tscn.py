import re

with open("scenes/Level.tscn", "r") as f:
    content = f.read()

# Add external resource for BaseItem
ext_resource = '[ext_resource type="PackedScene" uid="uid://itembase12345" path="res://scenes/BaseItem.tscn" id="4_item"]\n'
content = content.replace('[node name="Level" type="Node2D"]', ext_resource + '\n[node name="Level" type="Node2D"]')

# Add exported variables to LevelGenerator node
gen_node_replacement = """[node name="LevelGenerator" type="Node" parent="."]
script = ExtResource("3_gen")
items_root_path = NodePath("../ItemsRoot")
gold_scene = ExtResource("4_item")
rock_scene = ExtResource("4_item")"""

content = content.replace('[node name="LevelGenerator" type="Node" parent="."]\nscript = ExtResource("3_gen")\nitems_root_path = NodePath("../ItemsRoot")', gen_node_replacement)

with open("scenes/Level.tscn", "w") as f:
    f.write(content)
