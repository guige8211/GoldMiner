import re

with open("scripts/data/ItemDB.gd", "r") as f:
    content = f.read()

# I will append new items right before the closing brace of the UPGRADES dictionary.
new_items = """	
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
	}
"""

content = content.replace('\n\t"metronome"', new_items + '\n\t"metronome"')

with open("scripts/data/ItemDB.gd", "w") as f:
    f.write(content)
