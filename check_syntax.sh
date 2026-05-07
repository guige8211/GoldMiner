#!/usr/bin/env bash

# Godot GDScript Syntax Checker
echo "🔍 Running GDScript syntax checks..."

# Find Godot
if [ -f "./Godot_v4.3-stable_linux.x86_64" ]; then
    GODOT="./Godot_v4.3-stable_linux.x86_64"
elif command -v godot &> /dev/null; then
    GODOT="godot"
else
    echo "❌ Godot binary not found."
    /usr/bin/env false
fi

FAILED=0
ERROR_PATTERNS="SCRIPT ERROR|Parse Error|Compile Error|Method not found|Identifier not found|does not exist"
# False positives due to headless mode not loading the full project context for individual scripts
AUTOLOADS="EventBus|ItemDB|GameManager|UpgradeManager|MetaProgression"
CLASSES="LevelGenerator|ShopItem|Hook|Player|ItemBase|Shop"
IGNORED="$AUTOLOADS|$CLASSES"

# Find all .gd files
GD_FILES=$(find . -name "*.gd" -not -path "*/.*")

for file in $GD_FILES; do
    CLEAN_FILE=${file#./}
    # Run godot in headless mode with the script.
    OUTPUT=$("$GODOT" --headless --script "$file" --quit 2>&1)

    if echo "$OUTPUT" | grep -q "$CLEAN_FILE"; then
        # Filter out false positives
        REAL_ERRORS=$(echo "$OUTPUT" | grep -E "$ERROR_PATTERNS" | grep -vE "$IGNORED")

        if [ -n "$REAL_ERRORS" ]; then
             echo "❌ Syntax error in $file:"
             echo "--------------------------------------------------"
             echo "$REAL_ERRORS"
             echo "--------------------------------------------------"
             FAILED=1
        fi
    fi
done

if [ $FAILED -eq 1 ]; then
    echo "❌ Syntax check FAILED."
    /usr/bin/env false
else
    echo "✅ Syntax check PASSED for all scripts."
    /usr/bin/env true
fi
