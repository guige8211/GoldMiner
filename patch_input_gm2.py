import re

with open("project.godot", "r") as f:
    content = f.read()

# Add gm_time_skip to input map
gm_input2 = """gm_time_skip={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":84,"key_label":0,"unicode":116,"location":0,"echo":false,"script":null)
]
}
"""

if "gm_time_skip=" not in content:
    content = content.replace("gm_collect_all={", gm_input2 + "gm_collect_all={")

with open("project.godot", "w") as f:
    f.write(content)
