# AI Agent Instructions for Godot 4.3 Roguelite Gold Miner
# Godot 4.3 肉鸽黄金矿工 AI 代理指令

Welcome, AI Agent! When working on this repository, you **MUST** strictly adhere to the following rules to prevent code regressions, broken builds, and architectural drift.
欢迎，AI 代理！在此仓库工作时，你**必须**严格遵守以下规则，以防止代码退化、构建破坏和架构偏离。

## 1. Strict Code Editing Rules / 严苛的代码修改规范 (CRITICAL)
- **NO FULL-FILE OVERWRITES / 禁止全量覆写**: Never overwrite a file entirely unless creating a new one.
- **READ BEFORE DIFF / 先读取再修改**: ALWAYS read the current file state (`read_file` or `cat`) before proposing a change. Never rely on conversational memory.
- **PRECISE DIFFS / 精准 Diff 修改**: ALWAYS use precise git merge diff markers (`<<<<<<< SEARCH`, `=======`, `>>>>>>> REPLACE`) to modify existing files.
- **VERIFY EDITS / 验证修改**: After editing, inspect the file to ensure the diff was applied correctly and no logic was truncated.
- **LOW-LEVEL ERROR PREVENTION / 防止低级错误**: Double-check for "calling non-existent functions" or "misspelled variable names". This is a hard requirement.

## 2. Architectural Hard Rules / 架构硬性规定
To prevent "memory loss" regarding our core systems / 防止对核心系统的“遗忘”：

### 2.1 Dual Economy System / 双轨制经济系统
- **Score (分数)**: Resets every level. Used to hit the quota to pass the level.
  - USE: `GameManager.add_score(amount)`, `GameManager.current_score`.
- **Coins (金币)**: Persists across levels. Used to buy items in the Shop.
  - USE: `GameManager.add_coins(amount)`, `GameManager.current_coins`.
- **DEPRECATED / 禁止使用**: DO NOT use `add_gold`, `money`, or `gold`. These are strictly forbidden.

### 2.2 EventBus Architecture / EventBus 架构
- **DECOUPLING / 解耦**: All major gameplay interactions and value modifications MUST go through `scripts/singletons/EventBus.gd`.
- **MODIFIERS / 修饰器**: Any modification to item values, retract speeds, or player stats from Upgrades/Items MUST be handled via signals (e.g., `EventBus.request_item_value_modifiers`).
- **NO HARDCODING / 禁止硬编码**: Do not hardcode specific upgrade logic inside `GameManager.gd` or `ItemBase.gd`. Use the EventBus to intercept and modify values dynamically.

## 3. Pre-Commit Validation / 提交前验证
Before pushing code or using the `submit` tool:
- **SYNTAX CHECK / 语法检查**: Run `./check_syntax.sh` to verify GDScript syntax. This tool catches "calling non-existent functions" and parse errors.
- **TSCNS / 场景文件**: If you modify `.tscn` files, ensure the Godot-specific formatting remains intact.

## 4. UI/Web Testing Constraints / UI与Web测试约束
- Automated tests run headless. Use `Input.action_press()` or console log scraping to verify UI behavior.
