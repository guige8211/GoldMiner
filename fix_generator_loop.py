with open("scripts/systems/LevelGenerator.gd", "r") as f:
    content = f.read()

# I see the error: "ERROR: Scene for gold_large is NULL!"
# The problem is that when LevelGenerator is instantiated in the scene tree, Godot assigns exports
# BUT we override them if we try to initialize them in a bad way. 
# Wait, no. `gold_large_scene` is an exported variable.
# BUT I removed `_ready()`, and I am initializing `ITEMS` inside `generate_level`.
# If `gold_large_scene` is null, it means the inspector didn't save the reference correctly,
# OR the file path is wrong.
# Let's check scenes/items/GoldLarge.tscn.
# "path="res://scenes/items/GoldLarge.tscn""
# Does it exist? Yes.
# Why does Godot fail to load it?
# Because the `uid://gold_large_uid` might be invalid, so Godot fails to map the PackedScene.
# Let's remove the explicit uid from Level.tscn to force Godot to use the path instead.

with open("scenes/Level.tscn", "r") as f:
    scene_content = f.read()

# Remove uids from the item packed scenes so it falls back to path loading
scene_content = scene_content.replace(' uid="uid://gold_small_uid"', '')
scene_content = scene_content.replace(' uid="uid://gold_large_uid"', '')
scene_content = scene_content.replace(' uid="uid://rock_uid"', '')
scene_content = scene_content.replace(' uid="uid://diamond_uid"', '')

with open("scenes/Level.tscn", "w") as f:
    f.write(scene_content)
