import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv
import pandas as pd

# the goal of this code is to get score data for each quarter for each super bowl
root_url = 'https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions'
resp = requests.get(root_url)
soup = BeautifulSoup(resp.content, "html.parser")
table = soup.find_all("table")
# pprint(table[1])
super_bowl_links = table[1].find_all('a')
# print(super_bowl_links)
links = [super_bowl.get("href") for super_bowl in super_bowl_links]

# hrefs contains all sublinks to each super bowl
sublinks=[]
pattern = r'\/wiki\/Super_Bowl_.*'
for href in links:
	match = re.findall(pattern, href)
	# print(match)
	if len(match) != 0:
		sublinks.append(match[0])
# print(sublinks)
# links contains all links to each super bowl
links = ["https://en.wikipedia.org" + sublink for sublink in sublinks]
# print(links)
game_info = []
for link in links[:len(links)-4]:
	# print(link)
	resp = requests.get(link)
	soup = BeautifulSoup(resp.content, "html.parser")
	table = soup.find_all("table", attrs = {'class':'wikitable', 'style':'font-size:95%; margin-left:1em; float:right'})
	game_score = []
	team_score = []
	try:
		if link[-3:] == '_LI':
			for item in table[0].find_all("td"):
				team_score.append(item.text)
				if len(team_score) == 7:
					del team_score[-1]
					game_score.append(team_score)
					team_score = []
					if len(game_score) == 2:
						game_info.append(game_score)
						game_score = []
		else:
			for item in table[0].find_all("td"):
				team_score.append(item.text)
				if len(team_score) == 6:
					game_score.append(team_score)
					team_score = []
					if len(game_score) == 2:
						game_info.append(game_score)
						game_score = []
	except:
		print(link)
		continue
# turn strings to integer for later calculation
for game in game_info:
	for team in game:
		del team[0]
		print(team)
		for i in range(len(team)):
			team[0] = int(team[0])
			team[1] = int(team[1])
			team[2] = int(team[2])
			team[3] = int(team[3])
			team[4] = int(team[4])
# pprint(game_info)
game_info1 = []
for game in game_info:
	game = game[0] + (game[1])
	game_info1.append(game)
# pprint(game_info1)
df = pd.DataFrame(game_info1, columns = ['team1_1Q', 'team1_2Q', 'team1_3Q', 'team1_4Q', 'team1_F',\
										'team2_1Q', 'team2_2Q', 'team2_3Q', 'team2_4Q', 'team2_F'])
# print(df)
# competitive_score is calculated by the average point difference for every quarter (not cumulative)
df['competitive_score'] = round(sum((abs(df['team1_1Q']-df['team2_1Q']), abs(df['team1_2Q']-df['team2_2Q']) \
							,abs(df['team1_3Q']-df['team2_3Q']), abs(df['team1_4Q']-df['team2_4Q']))) / 4, 4)
# print(df)
print(df.shape)
df.to_csv("competitiveness.csv")








