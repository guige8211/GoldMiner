with open("scripts/player/Hook.gd", "r") as f:
    content = f.read()

content = content.replace("export var max_length: float = 600.0", "export var max_length: float = 800.0")

with open("scripts/player/Hook.gd", "w") as f:
    f.write(content)
