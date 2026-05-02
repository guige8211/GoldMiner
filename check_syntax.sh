#!/usr/bin/env bash

# Simple script to check GDScript syntax using Godot's headless mode
echo "Running GDScript syntax checks..."

GODOT_BIN="./Godot_v4.3-stable_linux.x86_64"

if [ ! -f "$GODOT_BIN" ]; then
    echo "Downloading Godot for local syntax check..."
    wget -q -O godot.zip "https://github.com/godotengine/godot/releases/download/4.3-stable/Godot_v4.3-stable_linux.x86_64.zip"
    unzip -q godot.zip
    chmod +x $GODOT_BIN
    rm godot.zip
fi

# Run the editor once to build solutions
OUTPUT=$($GODOT_BIN --headless --build-solutions --quit 2>&1)

# Check the output for compile errors
if echo "$OUTPUT" | grep -qE "SCRIPT ERROR|Parse Error|Compile Error"; then
    echo "Syntax check FAILED. Errors found:"
    echo "$OUTPUT" | grep -A 2 -E "SCRIPT ERROR|Parse Error|Compile Error"
    # End script with non-zero status
    /usr/bin/env false
else
    echo "Syntax check PASSED. All scripts compiled successfully."
    # End script with zero status
    /usr/bin/env true
fi
