with open("scripts/data/ItemDB.gd", "r") as f:
    content = f.read()

# Error: "Parse Error: Class "ItemDB" hides an autoload singleton."
# Godot 4 throws this error if you have `class_name ItemDB` AND an autoload named `ItemDB`.
# Since I added ItemDB as an autoload to avoid other issues, I must remove `class_name ItemDB`.

content = content.replace("class_name ItemDB\n", "")

with open("scripts/data/ItemDB.gd", "w") as f:
    f.write(content)

with open("project.godot", "r") as f:
    proj = f.read()

# Error: "Attempt to open script 'res://scripts/singletons/EventBus.gd' resulted in error 'File not found'."
# Why? Is EventBus.gd not tracked by git or named differently?
import os
print("Does EventBus exist?", os.path.exists("scripts/singletons/EventBus.gd"))
