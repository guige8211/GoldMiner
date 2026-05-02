extends Node

class_name ItemDB

const UPGRADES = {
	# --- BASE / STATIC UPGRADES ---
	"oil_can": {
		"name": "Oil Can",
		"desc": "Increases base hook speed by 20%.",
		"price": 2,
		"type": "static",
		"stat": "hook_speed_multiplier",
		"value": 0.2,
		"color": Color(0.6, 0.6, 0.6)
	},
	"lucky_clover": {
		"name": "Lucky Clover",
		"desc": "Increases the chance of Diamonds spawning.",
		"price": 5,
		"type": "static",
		"stat": "diamond_spawn_chance_bonus",
		"value": 0.15,
		"color": Color(0.2, 0.8, 0.2)
	},
	
	# --- TRASH / ALCHEMY BUILD ---
	"geologist": {
		"name": "Geologist",
		"desc": "Rocks are now worth 80 base score.",
		"price": 4,
		"type": "dynamic",
		"color": Color(0.4, 0.4, 0.4)
	},
	
	# --- ECONOMY BUILD ---
	"gold_rush": {
		"name": "Gold Rush",
		"desc": "Whenever you grab a small gold nugget, gain 1 Coin immediately.",
		"price": 4,
		"type": "dynamic",
		"color": Color(1.0, 0.9, 0.0)
	},
	"greedy_pot": {
		"name": "Greedy Pot",
		"desc": "Increases max interest cap from 5 to 15.",
		"price": 6,
		"type": "dynamic",
		"color": Color(0.8, 0.6, 0.1)
	},
	"appraisal": {
		"name": "Appraisal",
		"desc": "All items give +30 flat score.",
		"price": 3,
		"type": "dynamic",
		"color": Color(0.6, 0.8, 1.0)
	},
	
	# --- TIME BUILD ---
	"pocket_watch": {
		"name": "Pocket Watch",
		"desc": "Every item grabbed adds 2 seconds to the clock.",
		"price": 6,
		"type": "dynamic",
		"color": Color(0.9, 0.9, 0.8)
	},
	"finale": {
		"name": "Grand Finale",
		"desc": "In the last 10 seconds of a run, all items are worth 2x score.",
		"price": 8,
		"type": "dynamic",
		"color": Color(1.0, 0.3, 0.3)
	},
	
	# --- COMBO BUILD ---	
	# --- DEMOLITION BUILD ---
	"rock_crusher": {
		"name": "碎石机",
		"desc": "拉回【石头】时不再受到重力减速惩罚，反而拉回速度提升 50%。",
		"price": 5,
		"type": "dynamic",
		"color": Color(0.8, 0.3, 0.2)
	},
	
	# --- SNIPER BUILD ---
	"heavy_anchor": {
		"name": "沉甸甸的锚",
		"desc": "钩爪的左右摇摆速度变慢 40%（更容易瞄准小目标）。",
		"price": 3,
		"type": "static",
		"stat": "hook_swing_multiplier",
		"value": -0.4,
		"color": Color(0.2, 0.3, 0.4)
	},
	
	# --- COMBO & TIME EXPANSION ---
	"adrenaline": {
		"name": "肾上腺素",
		"desc": "出钩速度大幅提升 40%。但如果抓到石头，倒计时直接扣 5 秒！",
		"price": 6,
		"type": "dynamic",
		"color": Color(0.9, 0.2, 0.5)
	},
	
	# --- T3 SYNERGY / EMERGENT BUILD ---
	"wildcard": {
		"name": "万能标签",
		"desc": "你的所有物品触发类卡牌（如“抓小金块加钱”、“抓石头变80分”），现在抓取【任何物品】均可触发！",
		"price": 18,
		"type": "dynamic",
		"color": Color(1.0, 1.0, 1.0)
	},
	"compound_interest": {
		"name": "资本复利",
		"desc": "利息不再受上限限制，而是按你当前总资产的 10% 直接发放分红！",
		"price": 20,
		"type": "dynamic",
		"color": Color(1.0, 0.8, 0.4)
	},
	"metronome": {
		"name": "Metronome",
		"desc": "Each successful consecutive grab makes the hook 10% faster. Resets on miss.",
		"price": 5,
		"type": "dynamic",
		"color": Color(0.8, 0.4, 0.8)
	}
}

static func get_upgrade(id: String) -> Dictionary:
	if UPGRADES.has(id):
		var u = UPGRADES[id].duplicate()
		u["id"] = id
		return u
	return {}

static func get_random_upgrades(count: int, ignore_list: Array = []) -> Array:
	var pool = UPGRADES.keys()
	var result = []
	pool.shuffle()
	
	for id in pool:
		if not ignore_list.has(id):
			result.append(get_upgrade(id))
		if result.size() >= count:
			break
			
	return result
