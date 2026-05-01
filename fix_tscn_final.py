import re

with open("scenes/Level.tscn", "r") as f:
    content = f.read()

# Replace the base item with the specific items
old_res = '[ext_resource type="PackedScene" uid="uid://itembase12345" path="res://scenes/BaseItem.tscn" id="4_item"]'

new_res = """[ext_resource type="PackedScene" uid="uid://gold_small_uid" path="res://scenes/items/GoldSmall.tscn" id="4_gold_small"]
[ext_resource type="PackedScene" uid="uid://gold_large_uid" path="res://scenes/items/GoldLarge.tscn" id="5_gold_large"]
[ext_resource type="PackedScene" uid="uid://rock_uid" path="res://scenes/items/Rock.tscn" id="6_rock"]
[ext_resource type="PackedScene" uid="uid://diamond_uid" path="res://scenes/items/Diamond.tscn" id="7_diamond"]"""

content = content.replace(old_res, new_res)

old_node = """[node name="LevelGenerator" type="Node" parent="."]
script = ExtResource("3_gen")
items_root_path = NodePath("../ItemsRoot")
gold_scene = ExtResource("4_item")
rock_scene = ExtResource("4_item")"""

new_node = """[node name="LevelGenerator" type="Node" parent="."]
script = ExtResource("3_gen")
items_root_path = NodePath("../ItemsRoot")
gold_small_scene = ExtResource("4_gold_small")
gold_large_scene = ExtResource("5_gold_large")
rock_scene = ExtResource("6_rock")
diamond_scene = ExtResource("7_diamond")"""

content = content.replace(old_node, new_node)
content = content.replace("load_steps=4", "load_steps=8")

with open("scenes/Level.tscn", "w") as f:
    f.write(content)
