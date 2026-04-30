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
