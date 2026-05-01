mkdir -p scenes/items

cat << 'INNER_EOF' > scenes/items/GoldSmall.tscn
[gd_scene load_steps=4 format=3 uid="uid://gold_small_uid"]
[ext_resource type="Script" path="res://scripts/items/ItemBase.gd" id="1_item"]
[sub_resource type="PlaceholderTexture2D" id="PlaceholderTexture2D_item"]
size = Vector2(25, 25)
[sub_resource type="RectangleShape2D" id="RectangleShape2D_item"]
size = Vector2(25, 25)
[node name="GoldSmall" type="Area2D"]
script = ExtResource("1_item")
item_name = "Small Gold"
base_value = 50
weight = 1.0
[node name="Sprite2D" type="Sprite2D" parent="."]
modulate = Color(1, 0.843137, 0, 1)
texture = SubResource("PlaceholderTexture2D_item")
[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_item")
INNER_EOF

cat << 'INNER_EOF' > scenes/items/GoldLarge.tscn
[gd_scene load_steps=4 format=3 uid="uid://gold_large_uid"]
[ext_resource type="Script" path="res://scripts/items/ItemBase.gd" id="1_item"]
[sub_resource type="PlaceholderTexture2D" id="PlaceholderTexture2D_item"]
size = Vector2(60, 60)
[sub_resource type="RectangleShape2D" id="RectangleShape2D_item"]
size = Vector2(60, 60)
[node name="GoldLarge" type="Area2D"]
script = ExtResource("1_item")
item_name = "Large Gold"
base_value = 250
weight = 3.5
[node name="Sprite2D" type="Sprite2D" parent="."]
modulate = Color(1, 0.74902, 0, 1)
texture = SubResource("PlaceholderTexture2D_item")
[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_item")
INNER_EOF

cat << 'INNER_EOF' > scenes/items/Rock.tscn
[gd_scene load_steps=4 format=3 uid="uid://rock_uid"]
[ext_resource type="Script" path="res://scripts/items/ItemBase.gd" id="1_item"]
[sub_resource type="PlaceholderTexture2D" id="PlaceholderTexture2D_item"]
size = Vector2(45, 45)
[sub_resource type="RectangleShape2D" id="RectangleShape2D_item"]
size = Vector2(45, 45)
[node name="Rock" type="Area2D"]
script = ExtResource("1_item")
item_name = "Rock"
type = 1
base_value = 10
weight = 5.0
[node name="Sprite2D" type="Sprite2D" parent="."]
modulate = Color(0.411765, 0.411765, 0.411765, 1)
texture = SubResource("PlaceholderTexture2D_item")
[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_item")
INNER_EOF

cat << 'INNER_EOF' > scenes/items/Diamond.tscn
[gd_scene load_steps=4 format=3 uid="uid://diamond_uid"]
[ext_resource type="Script" path="res://scripts/items/ItemBase.gd" id="1_item"]
[sub_resource type="PlaceholderTexture2D" id="PlaceholderTexture2D_item"]
size = Vector2(15, 15)
[sub_resource type="RectangleShape2D" id="RectangleShape2D_item"]
size = Vector2(15, 15)
[node name="Diamond" type="Area2D"]
script = ExtResource("1_item")
item_name = "Diamond"
type = 2
base_value = 600
weight = 0.5
[node name="Sprite2D" type="Sprite2D" parent="."]
modulate = Color(0, 0.866667, 1, 1)
texture = SubResource("PlaceholderTexture2D_item")
[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_item")
INNER_EOF
