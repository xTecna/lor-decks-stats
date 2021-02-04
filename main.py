import csv
import requests

total_regions = {
    "demacia": 0,
	"freljord": 0,
	"ionia": 0,
	"noxus": 0,
	"piltoverzaun": 0,
	"shadowisles": 0,
	"bilgewater": 0,
	"targon": 0
}

translate_regions = {
	"demacia": "Demacia",
	"freljord": "Freljord",
	"ionia": "Ionia",
	"noxus": "Noxus",
	"piltoverzaun": "Piltover & Zaun",
	"shadowisles": "Shadow Isles",
	"bilgewater": "Bilgewater",
	"targon": "Targon"
}

total_champions = {
    "Lucian": 0,
	"Heimerdinger": 0,
	"Braum": 0,
	"Darius": 0,
	"Jinx": 0,
	"Fiora": 0,
	"Elise": 0,
	"Kalista": 0,
	"Ashe": 0,
	"Draven": 0,
	"Ezreal": 0,
	"Thresh": 0,
	"Teemo": 0,
	"Yasuo": 0,
	"Zed": 0,
	"Shen": 0,
	"Karma": 0,
	"Tryndamere": 0,
	"Katarina": 0,
	"Vladimir": 0,
	"Hecarim": 0,
	"Anivia": 0,
	"Lux": 0,
	"Garen": 0,
	"Gangplank": 0,
	"MissFortune": 0,
	"LeeSin": 0,
	"Sejuani": 0,
	"Maokai": 0,
	"Vi": 0,
	"Swain": 0,
	"Nautilus": 0,
	"TwistedFate": 0,
	"Fizz": 0,
	"Quinn": 0,
	"Taric": 0,
	"Leona": 0,
	"Lulu": 0,
	"Nocturne": 0,
	"AurelionSol": 0,
	"Trundle": 0,
	"Diana": 0,
	"Shyvana": 0,
	"Soraka": 0,
	"TahmKench": 0,
	"Zoe": 0,
	"Riven": 0,
	"Viktor": 0,
	"Aphelios": 0
}

translate_champions = {
	"MissFortune": "Miss Fortune",
	"LeeSin": "Lee Sin",
	"TwistedFate": "Twisted Fate",
	"AurelionSol": "Aurelion Sol",
	"TahmKench": "Tahm Kench",
}

decks = []

with open('input.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		for deck in row[2:]:
			if (deck == ''):
				print('Encontrado um deck vazio pelo jogador {0}.'.format(row[0]))
				continue

			r = requests.get('https://escolaruneterra.herokuapp.com/deck/decode?deck={0}&locale=pt_br'.format(deck))
			if (r.status_code == 200):
				data = r.json()

			for region in data['regions']:
				total_regions[region] += 1

			for champion in data['champions']:
				total_champions[champion] += 1

with open('output_regions.csv', mode='w', newline='') as regions_file:
	regions_writer = csv.writer(regions_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	for region in total_regions:
		regions_writer.writerow([translate_regions[region], total_regions[region]])

with open('output_champions.csv', mode='w', newline='') as champions_file:
	champions_writer = csv.writer(champions_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	for champion in total_champions:
		if (total_champions[champion] > 0):
			champions_writer.writerow([translate_champions[champion] if champion in translate_champions else champion, total_champions[champion]])
