import re

with open("project.godot", "r") as f:
    content = f.read()

# Add gm_collect_all to input map
gm_input = """gm_collect_all={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":75,"key_label":0,"unicode":107,"location":0,"echo":false,"script":null)
]
}
"""

if "gm_collect_all=" not in content:
    content = content.replace("[input]\n", "[input]\n\n" + gm_input)

with open("project.godot", "w") as f:
    f.write(content)
