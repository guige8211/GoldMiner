with open("build.sh", "r") as f:
    content = f.read()

# I see the problem! "Failed loading resource: Make sure resources have been imported by opening the project in the editor at least once."
# Godot 4 REQUIRES you to run the editor ONCE in headless mode to import all resources (.import files) 
# BEFORE running the export command, otherwise the export doesn't pack them properly.

new_build = """# 3. Build HTML5
echo "Importing resources..."
$GODOT_BIN --headless --editor --quit

echo "Exporting to HTML5..."
mkdir -p public
$GODOT_BIN --headless --export-release "Web" ./public/index.html"""

content = content.replace("""# 3. Build HTML5
echo "Exporting to HTML5..."
mkdir -p public
$GODOT_BIN --headless --export-release "Web" ./public/index.html""", new_build)

with open("build.sh", "w") as f:
    f.write(content)
