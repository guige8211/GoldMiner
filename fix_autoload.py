with open("project.godot", "r") as f:
    content = f.read()

# I see it: "Identifier 'EventBus' not declared" because EventBus is missing from [autoload]!
# I remember adding it in a patch (`EventBus="*res://scripts/singletons/EventBus.gd"`),
# but my massive git commit conflicts must have overwritten project.godot and erased it.

old_autoload = """[autoload]

GameManager="*res://scripts/singletons/GameManager.gd"
UpgradeManager="*res://scripts/singletons/UpgradeManager.gd"
MetaProgression="*res://scripts/singletons/MetaProgression.gd\""""

new_autoload = """[autoload]

EventBus="*res://scripts/singletons/EventBus.gd"
ItemDB="*res://scripts/data/ItemDB.gd"
GameManager="*res://scripts/singletons/GameManager.gd"
UpgradeManager="*res://scripts/singletons/UpgradeManager.gd"
MetaProgression="*res://scripts/singletons/MetaProgression.gd\""""

content = content.replace(old_autoload, new_autoload)

with open("project.godot", "w") as f:
    f.write(content)
