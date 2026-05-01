with open("scripts/data/ItemDB.gd", "r") as f:
    content = f.read()

# We need to manually adjust the prices based on the new logic.
# Original prices:
# oil_can: 3 -> 2
# lucky_clover: 8 -> 5
# geologist: 5 -> 4
# gold_rush: 5 -> 4
# greedy_pot: 8 -> 6
# appraisal: 4 -> 3
# pocket_watch: 10 -> 6
# finale: 12 -> 8
# metronome: 8 -> 5

replacements = {
    '"name": "Oil Can",\n\t\t"desc": "Increases base hook speed by 20%.",\n\t\t"price": 3,': '"name": "Oil Can",\n\t\t"desc": "Increases base hook speed by 20%.",\n\t\t"price": 2,',
    '"name": "Lucky Clover",\n\t\t"desc": "Increases the chance of Diamonds spawning.",\n\t\t"price": 8,': '"name": "Lucky Clover",\n\t\t"desc": "Increases the chance of Diamonds spawning.",\n\t\t"price": 5,',
    '"name": "Geologist",\n\t\t"desc": "Rocks are now worth 80 base score.",\n\t\t"price": 5,': '"name": "Geologist",\n\t\t"desc": "Rocks are now worth 80 base score.",\n\t\t"price": 4,',
    '"name": "Gold Rush",\n\t\t"desc": "Whenever you grab a small gold nugget, gain 1 Coin immediately.",\n\t\t"price": 5,': '"name": "Gold Rush",\n\t\t"desc": "Whenever you grab a small gold nugget, gain 1 Coin immediately.",\n\t\t"price": 4,',
    '"name": "Greedy Pot",\n\t\t"desc": "Increases max interest cap from 5 to 15.",\n\t\t"price": 8,': '"name": "Greedy Pot",\n\t\t"desc": "Increases max interest cap from 5 to 15.",\n\t\t"price": 6,',
    '"name": "Appraisal",\n\t\t"desc": "All items give +30 flat score.",\n\t\t"price": 4,': '"name": "Appraisal",\n\t\t"desc": "All items give +30 flat score.",\n\t\t"price": 3,',
    '"name": "Pocket Watch",\n\t\t"desc": "Every item grabbed adds 2 seconds to the clock.",\n\t\t"price": 10,': '"name": "Pocket Watch",\n\t\t"desc": "Every item grabbed adds 2 seconds to the clock.",\n\t\t"price": 6,',
    '"name": "Grand Finale",\n\t\t"desc": "In the last 10 seconds of a run, all items are worth 2x score.",\n\t\t"price": 12,': '"name": "Grand Finale",\n\t\t"desc": "In the last 10 seconds of a run, all items are worth 2x score.",\n\t\t"price": 8,',
    '"name": "Metronome",\n\t\t"desc": "Each successful consecutive grab makes the hook 10% faster. Resets on miss.",\n\t\t"price": 8,': '"name": "Metronome",\n\t\t"desc": "Each successful consecutive grab makes the hook 10% faster. Resets on miss.",\n\t\t"price": 5,'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open("scripts/data/ItemDB.gd", "w") as f:
    f.write(content)
