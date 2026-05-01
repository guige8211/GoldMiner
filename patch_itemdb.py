with open("scripts/data/ItemDB.gd", "r") as f:
    content = f.read()

# Scale down prices
content = content.replace('"price": 100,', '"price": 3,')
content = content.replace('"price": 250,', '"price": 8,')
content = content.replace('"price": 150,', '"price": 5,')
content = content.replace('"price": 300,', '"price": 10,')
content = content.replace('"price": 400,', '"price": 12,')

# Add Economy Cards
eco_cards = """	# --- ECONOMY BUILD ---
	"gold_rush": {
		"name": "Gold Rush",
		"desc": "Whenever you grab a small gold nugget, gain 1 Coin immediately.",
		"price": 5,
		"type": "dynamic",
		"color": Color(1.0, 0.9, 0.0)
	},
	"greedy_pot": {
		"name": "Greedy Pot",
		"desc": "Increases max interest cap from 5 to 15.",
		"price": 8,
		"type": "dynamic",
		"color": Color(0.8, 0.6, 0.1)
	},
	"appraisal": {
		"name": "Appraisal",
		"desc": "All items give +30 flat score.",
		"price": 4,
		"type": "dynamic",
		"color": Color(0.6, 0.8, 1.0)
	},
"""
content = content.replace('\t# --- TIME BUILD ---', eco_cards + '\t# --- TIME BUILD ---')

with open("scripts/data/ItemDB.gd", "w") as f:
    f.write(content)
