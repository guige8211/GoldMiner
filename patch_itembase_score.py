with open("scripts/items/ItemBase.gd", "r") as f:
    content = f.read()

content = content.replace("GameManager.add_gold(final_value)", "GameManager.add_score(final_value)")

with open("scripts/items/ItemBase.gd", "w") as f:
    f.write(content)
