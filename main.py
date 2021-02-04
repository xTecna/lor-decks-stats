import sys
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
	"shadowisles": "Ilhas das Sombras",
	"bilgewater": "Águas de Sentina",
	"targon": "Monte Targon"
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

def readFromCsvFile(import_filename):
	with open(import_filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')

		for row in csv_reader:
			for deck in row[2:]:
				if (deck == ''):
					print('Um deck vazio encontrado pelo jogador {0}.'.format(row[0]))
					continue
				
				r = requests.get('https://escolaruneterra.herokuapp.com/deck/decode?deck={0}&locale=pt_br'.format(deck))
				if (r.status_code == 200):
					data = r.json()

					for region in data['regions']:
						total_regions[region] += 1

					for champion in data['champions']:
						total_champions[champion] += 1

def exportToCsvFile(export_filename, total, translate):
	with open(export_filename, mode='w', newline='', encoding='utf-8') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		for item in total:
			csv_writer.writerow([translate[item] if item in translate else item, total[item]])

def sortGreater(total):
	return {k: v for k, v in sorted(total.items(), key=lambda item: item[1])[::-1]}

if (len(sys.argv) != 4):
	print('Precisa-se dos nomes do arquivo de entrada e dos arquivos de saída.')
else:
	readFromCsvFile(sys.argv[1])
	total_champions = sortGreater(total_champions)
	total_regions = sortGreater(total_regions)
	exportToCsvFile(sys.argv[2], total_champions, translate_champions)
	exportToCsvFile(sys.argv[3], total_regions, translate_regions)
