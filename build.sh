#!/bin/bash
set -e
echo "Starting build process for Godot HTML5 export..."

# 1. Download Godot Engine
GODOT_VERSION="4.3"
GODOT_URL="https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}-stable/Godot_v${GODOT_VERSION}-stable_linux.x86_64.zip"
echo "Downloading Godot ${GODOT_VERSION} from ${GODOT_URL}..."
wget -q -O godot.zip $GODOT_URL
unzip -q godot.zip
GODOT_BIN="./Godot_v${GODOT_VERSION}-stable_linux.x86_64"
chmod +x $GODOT_BIN

# 2. Download Godot Export Templates
TEMPLATE_URL="https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}-stable/Godot_v${GODOT_VERSION}-stable_export_templates.tpz"
echo "Downloading Godot templates from ${TEMPLATE_URL}..."
wget -q -O templates.tpz $TEMPLATE_URL

# Extract templates to the correct location
mkdir -p ~/.local/share/godot/export_templates/${GODOT_VERSION}.stable
unzip -q templates.tpz -d temp_templates
mv temp_templates/templates/* ~/.local/share/godot/export_templates/${GODOT_VERSION}.stable/
rm -rf temp_templates

# 3. Build HTML5
echo "Importing resources..."
$GODOT_BIN --headless --editor --quit

echo "Exporting to HTML5..."
mkdir -p public
$GODOT_BIN --headless --export-release "Web" ./public/index.html

echo "Build complete! Output is in the 'public' directory."
