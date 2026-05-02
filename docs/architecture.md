# 肉鸽版黄金矿工 (Rogue Miner) 架构设计文档

## 1. 核心游戏循环 (Game Loops)

### 1.1 局内循环 (In-Run Loop)
- **关卡阶段 (Level Phase):**
  - 玩家拥有固定的时间（例如60秒）进行抓取。
  - 需要达到本关的**目标金额 (Quota)**。
  - 地图中生成金块、石头、钻石、宝箱，以及干扰的机关/怪物。
  - 抓取结束后判定：
    - 未达到 Quota -> 游戏结束 (Game Over)，结算获得 Meta 资源。
    - 达到 Quota -> 进入结算阶段。
- **结算/商店阶段 (Shop/Upgrade Phase):**
  - 玩家打开在上一关中抓取到的**宝箱**，获得随机局内能力/属性提升。
  - 玩家使用本关赚取的**金币**，在商店购买随机刷出的道具/遗物。
  - 进入下一关卡，难度（Quota、垃圾数量、小怪）提升。

### 1.2 局外循环 (Meta Loop)
- 玩家游戏结束（Run失败）后，保留特定的资源（如天赋点数）。
- 在主界面可以进入“天赋树/升级”界面。
- 消耗资源提升永久能力（如初始钩子速度增加、商店物品打折、开局自带少量金币等）。

## 2. 核心系统与单例 (Singletons / Autoloads)

Godot 项目通过配置在 `project.godot` 中的全局脚本来管理核心状态：

- **`GameManager`**: 管理当前 Run 的状态。
  - 属性：当前金币 (Current Gold)，目标金额 (Target Quota)，当前关卡层数 (Level)，关卡倒计时 (Timer)。
  - 职责：判断胜负、触发阶段转换（关卡 -> 商店 -> 关卡）。
- **`UpgradeManager`**: 管理玩家在单局游戏内的成长体系 (Build)。
  - 属性：持有道具列表，属性加成修饰器 (Modifiers，例如 `hook_speed_multiplier`, `gold_value_multiplier`)。
  - 职责：应用宝箱开出的能力、处理商店购买逻辑。
- **`MetaProgression`**: 管理永久养成。
  - 属性：永久资源数量，已解锁的天赋字典。
  - 职责：存档/读档，提供基础属性加成（被 `UpgradeManager` 继承或叠加）。

## 3. 场景节点架构 (Node Hierarchy)

主要的场景包括：`Main.tscn` (负责场景切换), `Level.tscn` (关卡场景), `Shop.tscn` (商店场景).

### `Level.tscn` 的典型节点结构：
```text
Level (Node2D)
├── Camera2D
├── UI (CanvasLayer)
│   ├── TopHUD (Control - 现实金币、Quota、时间)
│   └── EndLevelPanel (Control - 关卡结束时的UI展示)
├── Environment (Node2D)
│   ├── Player (Node2D)
│   │   ├── Sprite2D (矿工形象)
│   │   └── Hook (Node2D/CharacterBody2D)
│   │       ├── Line2D (绳索视觉)
│   │       ├── Sprite2D (钩爪视觉)
│   │       ├── CollisionArea (Area2D - 抓取判定)
│   │       └── GrabbedItemPosition (Marker2D - 抓到物品挂载点)
├── ItemsRoot (Node2D) - 存放所有生成的矿物/宝箱
└── LevelGenerator (Node) - 负责根据层数动态生成地图内容
```

## 4. 核心实体设计

### 4.1 Hook (钩子)
状态机设计，拥有四个主要状态：
- **IDLE/SWINGING**: 在一定角度（如 -75度 到 75度）内往复旋转。
- **EXTENDING**: 玩家按下按键，钩子向当前角度直线发射，速度受 `UpgradeManager` 加成。
- **RETRACTING**: 抓到物品或到达最大距离后回收。回收速度基准受所抓物品重量 (`weight`) 影响。

### 4.2 ItemBase (可抓取物基类)
作为所有矿物/石头的父类（继承自 `Area2D` 或包含 `Area2D`）。
- **属性**:
  - `item_name`: 物品名称
  - `base_value`: 基础价值 (金币)
  - `weight`: 重量（影响回收速度，越重越慢）
  - `type`: 类型枚举 (Gold, Rock, Diamond, Chest, Mystery)

### 4.3 LevelGenerator (关卡生成器)
- 根据 `GameManager.current_level` 计算难度系数。
- 使用权重随机算法决定生成的物品种类和数量。
- 在定义的矩形区域内随机防止物品，保证它们尽量不重叠（或允许轻微重叠增加抓取难度）。
- 后期引入 `Obstacles` 或 `Enemies` (如移动老鼠)，挂载独立 AI 脚本。

### 4.4 关卡数值与产出系统 (Level Generation & Value Mechanics)

我们使用了一个基于“预算池 (Budget Pool)”的严谨数值模型来保证游戏的难度曲线和容错率：

1. **预算因子 (K-Factor)**:
   - 核心公式：`总产出价值 = Target Quota * K_Factor`
   - K_Factor 初始值为 `1.5`，意味着系统保证场上生成的有价矿物（金块、钻石）总价值至少是过关目标的 1.5 倍，给予玩家选择和容错的空间。
   - 未来扩展：随着玩家在局外养成中获得分数加成，为了平衡，基础 K 值会通过 MetaProgression 逐渐减小（收紧局内容错）。

2. **权重分布与难度曲线 (Weighted Distribution & Difficulty Curve)**:
   - 系统利用总预算去抽取物品，直到预算耗尽。抽取不是纯随机，而是基于**难度系数（当前层数）**：
   - **低难度**：系统更倾向于分配“大金块”。大金块体积大、容易抓取，但极度消耗时间，适合作为新手的保底收益。
   - **高难度**：系统降低大金块的权重，大幅提升“小钻石”的生成几率。高难度要求玩家能够精准捕捉体积极小、但能够瞬间拉回且价值极高的物品。

3. **惩罚障碍物 (Hazards & Blockers)**:
   - **石头**的生成不占用“预算池”。
   - 系统会在放置完所有有价矿物后，根据层数额外洒下大量石头作为物理遮挡。
   - 为了防止矿物和石头完美重叠导致无法抓取，系统引入了**基于半径的防堆叠算法 (Anti-overlap check)**，生成器会尝试最多 50 次去寻找一个没有穿模的空白区域进行生成。

### 5.4 新手保护机制 (Early Game Balance)
为了防止由纯随机算法导致的早期极端难度（如第一关因满地石头导致无法过关）：
- **第一关绝对保护 (Level 1 Exemption)**：第一关在生成时，系统会强制将其内部的石头（Hazards）生成数量归零。
- **强制保底 (Guaranteed Drops)**：在第一关中，生成器在计算随机预算池之前，会强制在地图中注入 3 个“小金块”以确保即便是最糟糕的运气也有基础的抓取标靶。这奠定了该游戏平滑的新手上手体验。

### 5.4 扩展流派卡牌生态 (Extended Build Ecosystem)
除基础的属性卡外，系统通过 EventBus 实现了多种深度联动的特殊流派：
*   **爆破/破坏流 (Demolition Build)**: 以化解抓取惩罚为主。如【碎石机】，它通过拦截 `request_retract_speed_modifiers` 事件，直接抵消石头的重量系数，变废为宝。
*   **狙击/蓄力流 (Sniper Build)**: 改变玩家出钩节奏。如【沉甸甸的锚】，通过降低钩爪的基础摇摆速度（swing multiplier < 1.0），使得瞄准小目标（钻石）变得极为简单。
*   **涌现/质变流 (Synergy Build)**:
    *   **【万能标签】**: 通过在 `UpgradeManager` 底层封装 `_is_match` 判定函数。如果持有万能标签，所有的条件判定（如“抓取石头时...”或“抓取小金块时...”）将一律返回 `true`，触发跨流派的化学反应。
    *   **【资本复利】**: 在 `GameManager` 结算发薪阶段进行拦截，突破基础系统的利息上限卡口，提供无限制的指数级经济滚雪球能力。
