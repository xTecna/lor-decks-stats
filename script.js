const no_champion = 'No Champion';

const regions_header = ['Regions', 'Qty.'];
const champions_header = ['Champions', 'Qty.'];
let count_regions = {};
let count_champions = {};
let converted_count_regions = [];
let converted_count_champions = [];

function generateStats(){
	const inputElement = document.getElementById('stats_file');
	const offsetElement = document.getElementById('offset');
	const limitElement = document.getElementById('limit');
	const contentElement = document.getElementById('content');
	const offset = offsetElement.value;
	const limit = limitElement.value;

	count_regions = {};
	count_champions = {};
	converted_count_regions = [];
	converted_count_champions = [];

	renderLoading();

	Papa.parse(inputElement.files[0], {
		complete: async function(results) {
			const players = results.data;

			for (let i = 0; i < players.length; ++i){
				let decks = players[i];
				decks = decks.slice(offset, offset + limit);

				for (let j = 0; j < decks.length; ++j){
					let deck = decks[j];

					if (deck){
						const response = await fetch(`https://escolaruneterra.herokuapp.com/deck/decode?deck=${deck}&locale=pt_br`);

						if (response.ok){
							const result = await response.json();
							
							result.regions.forEach((region) => {
								region = translateRegion(region);

								if (region in count_regions){
									count_regions[region] += 1;
								}else{
									count_regions[region] = 1;
								}
							});

							result.champions.forEach((champion) => {
								champion = translateChampion(champion);

								if (champion in count_champions){
									count_champions[champion] += 1;
								}else{
									count_champions[champion] = 1;
								}
							});

							if (result.champions.length == 0){
								if (no_champion in count_champions){
									count_champions[no_champion] += 1;
								}else{
									count_champions[no_champion] = 1;
								}
							}
						}
					}
				}
			}

			contentElement.innerHTML = '';

			count_regions = sort(count_regions);
			count_champions = sort(count_champions);

			renderResults(count_regions, 'regions', regions_header, exportRegions, 'Export Regions');
			renderResults(count_champions, 'champions', champions_header, exportChampions, 'Export Champions');
		}
	});
}

function renderLoading(){
	const contentElement = document.getElementById('content');

	contentElement.innerHTML = '<h1><i class="fa fa-spinner fa-spin fa-fw"></i> Loading...</h1>';
}

function translateRegion(region){
	switch (region){
		case 'demacia': 		return 'Demacia';
		case 'freljord':		return 'Freljord';
		case 'ionia':			return 'Ionia';
		case 'noxus':			return 'Noxus';
		case 'piltoverzaun':	return 'Piltover & Zaun';
		case 'shadowisles':		return 'Shadow Isles';
		case 'bilgewater':		return 'Bilgewater';
		case 'targon':			return 'Mount Targon';
	}
}

function translateChampion(champion){
	switch (champion){
		case 'LeeSin':			return 'Lee Sin';
		case 'MissFortune':		return 'Miss Fortune';
		case 'TwistedFate':		return 'Twisted Fate';
		case 'TahmKench':		return 'Tahm Kench';
		case 'AurelionSol':		return 'Aurelion Sol';
		default:				return champion;
	}
}

function sort(dictionary){
	const array = [];

	for (let key in dictionary){
		array.push([key, dictionary[key]]);
	}

	array.sort(compare);
	
	const new_dictionary = {};
	for (let index in array){
		new_dictionary[array[index][0]] = array[index][1];
	}

	return new_dictionary;
}

function compare(a, b){
	if (a[1] < b[1]){
		return 1;
	} else if (a[1] > b[1]){
		return -1;
	} else {
		if (a[0] < b[0]){
			return -1;
		} else if (a[0] > b[0]){
			return 1
		} else {
			return 0;
		}
	}
}

function renderResults(results, id, header, exportFunction, exportText){
	const contentElement = document.getElementById('content');
	const resultElement = document.createElement('div');
	const buttonElement = document.createElement('button');

	resultElement.id = id;

	const tableElement = renderTable(id, header, results);
	resultElement.appendChild(tableElement);

	contentElement.appendChild(resultElement);

	buttonElement.id = `export_${id}`;
	buttonElement.className = 'button';
	buttonElement.onclick = exportFunction;
	buttonElement.appendChild(document.createTextNode(exportText));

	resultElement.appendChild(buttonElement);
}

function renderTable(id, header, body){
	const table = document.createElement('table');
	table.id = `table_${id}`;

	renderTableHead(table, header);
	renderTableBody(table, body);

	return table;
}

function renderTableHead(table, header){
	const thead = table.createTHead();
	const row = thead.insertRow();

	for (const index in header){
		const th = document.createElement('th');
		th.appendChild(document.createTextNode(header[index]));
		row.appendChild(th);
	}
}

function renderTableBody(table, body){
	const tbody = table.createTBody();

	for (const key in body){
		const row = tbody.insertRow();
		let td = document.createElement('td');
		td.appendChild(document.createTextNode(key));
		row.appendChild(td);
		td = document.createElement('td');
		td.appendChild(document.createTextNode(body[key]));
		row.appendChild(td);
		tbody.appendChild(row);
	}
}

function exportRegions(){
	converted_count_regions = convert(converted_count_regions, count_regions, regions_header);
	exportCSV(converted_count_regions, 'regions.csv');
}

function exportChampions(){
	converted_count_champions = convert(converted_count_champions, count_champions, champions_header);
	exportCSV(converted_count_champions, 'champions.csv');
}

function convert(variable, results, header){
	if (variable.length === 0){
		const [header1, header2] = header;

		for (const key in results){
			const item = {};

			item[header1] = key;
			item[header2] = results[key];
			
			variable.push(item);
		}

		return variable;
	}else{
		return variable;
	}
}

function exportCSV(variable, filename){
	const csv = Papa.unparse(variable, {header: false});
	
	const exportElement = document.createElement('a');
	exportElement.href = `data:text/csv;charset=utf-8,${encodeURI(csv)}`;
	exportElement.target = '_blank';
	exportElement.rel = 'noopener noreferrer';
	exportElement.download = filename;
	exportElement.click();

	exportElement.remove();
}