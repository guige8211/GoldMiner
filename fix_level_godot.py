with open("scripts/Level.gd", "r") as f:
    content = f.read()

# Fix the current_gold issue that wasn't properly patched in the previous step due to race conditions
content = content.replace("GameManager.current_gold == 0", "GameManager.current_score == 0")

with open("scripts/Level.gd", "w") as f:
    f.write(content)
