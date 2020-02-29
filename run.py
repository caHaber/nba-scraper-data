from urllib2 import urlopen
from bs4 import BeautifulSoup
import pandas as pd
# from selenium import webdriver
import csv
import pickle
import os.path
# NBA teams and their abbriviations
nba_teams = [['ATL', 'Atlanta Hawks'], ['BRK', 'Brooklyn Nets'], ['BOS', 'Boston Celtics'], ['CHO', 'Charlotte Hornets'], ['CHI', 'Chicago Bulls'], ['CLE', 'Cleveland Cavaliers'], ['DAL', 'Dallas Mavericks'], ['DEN', 'Denver Nuggets'], ['DET', 'Detroit Pistons'], ['GSW', 'Golden State Warriors'], ['HOU', 'Houston Rockets'], ['IND', 'Indiana Pacers'], ['LAC', 'Los Angeles Clippers'], ['LAL', 'Los Angeles Lakers'], ['MEM', 'Memphis Grizzlies'], ['MIA', 'Miami Heat'], ['MIL', 'Milwaukee Bucks'], ['MIN', 'Minnesota Timberwolves'], ['NOP', 'New Orleans Pelicans'], ['NYK', 'New York Knicks'], ['OKC', 'Oklahoma City Thunder'], ['ORL', 'Orlando Magic'], ['PHI', 'Philadelphia 76ers'], ['PHO', 'Phoenix Suns'], ['POR', 'Portland Trail Blazers'], ['SAC', 'Sacramento Kings'], ['SAS', 'San Antonio Spurs'], ['TOR', 'Toronto Raptors'], ['UTA', 'Utah Jazz'], ['WAS', 'Washington Wizards']]

missing_players = {'Gary Trent Jr': 'Gary Trent', 'Patrick Mills': 'Patty Mills'\
				   , 'Moe Harkless': 'Maurice Harkless', 'TJ Warren': 'T.J. Warren',\
				   'Raymond Spalding': 'Ray Spalding', 'Mo Bamba': 'Mohamed Bamba',\
				   'DJ Augustin': 'D.J. Augustin', 'Dennis Schroeder':'Dennis Schroder',\
				   'DJ Wilson': 'D.J. Wilson', 'CJ Miles':'C.J. Miles',\
				   'Louis Williams': 'Lou Williams', 'TJ Leaf': 'T.J. Leaf',\
				   'PJ Tucker': 'P.J. Tucker', 'Tim Hardaway Jr': 'Tim Hardaway',\
				   'Larry Nance Jr':'Larry Nance','JR Smith': 'J.R. Smith', 'Walter Lemon Jr':'Walt Lemon'\
				   ,'Devonte Graham': "Devonte' Graham ", "DeAndre Bembry":"DeAndre' Bembry",\
				   'Taurean Prince': 'Taurean Waller-Prince'}


def generate_player_stats():
	p_dict = {}
	with open('all_players_updated_feb29.csv', 'r') as csvfile:
		    reader = csv.reader(csvfile, delimiter=',')
		    for row in reader:
		    	name = row[1].split('\\')[0]
		    	p_dict[name] = {'Age': row[4], 'Pos': row[3], 'eFG%': row[16], 'PTS': row[18], 'GP': row[5]}

	with open('player_stats.pickle', 'wb') as handle:
    		pickle.dump(p_dict, handle)
    
    	return p_dict



pickle_path = 'player_stats.pickle'
player_dict = {}

# if os.path.isfile(pickle_path): 
# 	with open(pickle_path, 'rb') as handle:
#     		player_dict = pickle.load(handle)
# else:
player_dict = generate_player_stats()

header_stats = ['eFG%','Age','PTS','Pos','GP']

for team in nba_teams:
	# URL page we will scraping (see image above)
	print team
	url = "https://hoopshype.com/salaries/{}/".format(team[1].lower().replace(" ","_"))
	print url

	html = urlopen(url)

	soup = BeautifulSoup(html, features="html.parser")
	
	# use getText()to extract the text we need into a list
	headers = [th.getText() for th in soup.findAll('thead')[0].findAll("tr")[1].findAll("td")]

	for h in header_stats:
		headers.append(h)

	rows = soup.findAll('tr')

	player_stats = []
	for i in range(2, len(rows)-3):
		player = []

		for td in rows[i].findAll('td'):
			player.append(td.getText().replace(",","").replace("\t","").replace('\n',""))

		if len(player[0]) > 2:
			try: 
				stats = player_dict[player[0]]
				for h in header_stats:
					player.append(stats[h])
			except:
				try:
					stats = player_dict[missing_players[player[0]]]
					for h in header_stats:
						player.append(stats[h])
				except:
					print player[0]
			player_stats.append(player)
		else:
			break
	print(headers)
	print(player_stats)
	stats = pd.DataFrame(player_stats, columns = headers,)

	stats.to_csv("teams/{}.csv".format(team[1]), sep=',', encoding='utf-8', index=False, quoting=csv.QUOTE_NONE, quotechar='',  escapechar='\\')


