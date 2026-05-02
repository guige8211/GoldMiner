# AI Agent Instructions for Godot 4.3 Roguelite Gold Miner

Welcome, AI Agent! When working on this repository, you **MUST** strictly adhere to the following rules to prevent code regressions, broken builds, and architectural drift.

## 1. Code Editing Rules (CRITICAL)
- **NEVER use full-file overwrites** unless you are creating a completely new file.
- **ALWAYS use precise git merge diffs (`<<<<<<< SEARCH`, `=======`, `>>>>>>> REPLACE`)** to modify existing files.
- **ALWAYS read the current file state (`read_file` or `cat`) before proposing a change.** Never rely on your conversational memory of what the file looks like, as it may be outdated.
- **Verify your edits.** After editing, briefly inspect the file to ensure the diff was applied correctly without truncating other logic.

## 2. Architectural Constants
This project uses specific architectural patterns. Do not deviate from them:
- **Dual Economy**: There is `Score` (resets every level, used to hit quota) and `Coins` (persists, used to buy shop items).
- **Event-Driven**: Modifications to item values, shop prices, or player stats MUST go through `EventBus.gd` (e.g., `EventBus.request_item_value_modifiers`). Do not hardcode logic inside `GameManager` or `ItemBase`.
- **Method Names**: 
  - DO NOT use `add_gold`. It has been deprecated. Use `GameManager.add_score(amount)` and `GameManager.add_coins(amount)`.
  - DO NOT use `GameManager.money`. Use `GameManager.coins`.

## 3. Pre-Commit Validation
Before pushing any code to the repository or using the `submit` tool, you must ensure the code parses correctly.
- Run `./check_syntax.sh` (if available) to verify GDScript syntax.
- If you modify `project.godot` or any `.tscn` file, ensure you have not corrupted the Godot specific formatting.

## 4. UI/Web Testing Constraints
- The automated GitHub Pages deployment runs headless.
- You cannot see the screen. Any UI interactions must be simulated either via `Input.action_press()` in GDScript (like the GM tools 'K' and 'T') or using headless browser testing tools (Playwright/Puppeteer) combined with console log scraping.
