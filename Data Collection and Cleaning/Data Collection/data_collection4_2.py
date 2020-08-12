import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv
import pandas as pd
import numpy as np

# the goal of this code is to use web scrapingto get winning team season stats 
# I noticed that the table I want to get the data from has different style and different position in
# each winning team's link. As a result, I had a hard time getting all the data I want through program
# This program helps me to get every line of data I want except 12 lines out of 54.
# I have to manually enter data for those 12 lines.
# main features to scrape: season record, end of the season streak, points for and points against
root_url = 'https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions'
resp = requests.get(root_url)
soup = BeautifulSoup(resp.content, "html.parser")
table = soup.find_all("table")
# pprint(table[1])
super_bowl_links = table[1].find_all('a')
# print(super_bowl_links)
links = [super_bowl.get("href") for super_bowl in super_bowl_links]
# print(links)

hrefs = []
pattern = r'\w+(?=_season)_season'
for href in links:
	# print(href)
	match = re.findall(pattern, href)
	# print(match)
	if len(match) != 0 and 'NFL' not in match[0] and 'Football' not in match[0]:
	 	hrefs.append(match[0])
# print(len(hrefs))

# winning_list and losing_list contain sublink to winning teams season and losing teasm season
winning_list = [hrefs[i] for i in range(len(hrefs)) if i % 2 == 0]
losing_list = [hrefs[i] for i in range(len(hrefs)) if i % 2 == 1]
# print(winning_list)
# print(len(winning_list))
# print(losing_list)
# print(len(losing_list))

winning_links = ["https://en.wikipedia.org/wiki/" + sublink for sublink in winning_list]
losing_links = ["https://en.wikipedia.org/wiki/" + sublink for sublink in losing_list]
# save the losing_links for the next coding file to get the season stats for losing team
# array = np.array(losing_links)
# losing_links_tran = array.transpose()
df_losing = pd.DataFrame(losing_links)
df_losing.to_csv('losing_links.csv')

# print(winning_links)
# print(losing_links)

winning_pct = []
point_for = []
point_against = []
end_streak = []
for link in winning_links:
	# print(link)
	if 'Louis_Rams_season' in link:
		link = 'https://en.wikipedia.org/wiki/1999_St._Louis_Rams_season'
	resp = requests.get(link)
	soup = BeautifulSoup(resp.content, "html.parser")
	# print(len(winning_pct))
	# table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size: 95%;'})
	if len(winning_pct) >= 10 and len(winning_pct) < 14:
		table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size: 95%;'})
	elif len(winning_pct) >= 14 and len(winning_pct) < 15:
		table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size:95%; text-align:center'})
	elif len(winning_pct) == 21:
		table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size: 95%; text-align:center'})
	elif len(winning_pct) > 35:
		table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size: 95%;'})
	else:
		if link[35:-7].replace("_",' ') == 'Dallas Cowboys' or link[35:-7].replace("_",' ') == 'Pittsburgh Steelers':
			table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size: 95%; text-align:center'})
		else:
			table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size:95%; text-align:center'})
	# pprint(table)
	try:
		if link[35:-7].replace("_",' ') == 'New York Jets':
			for item in table[1].find_all('tr'):
			# print(len(item.find_all('td')))
				for i in range(len(item.find_all('td'))):
					# print(item.find_all('td')[i].text.strip('\n\n'))
					# print(link[35:-7].replace("_",' '))
					if item.find_all('td')[i].text.strip('\n\n') == link[35:-7].replace("_",' '):
						winning_pct.append(item.find_all('td')[4].text.strip())
						point_for.append(item.find_all('td')[-3].text.strip())
						point_against.append(item.find_all('td')[-2].text.strip())
						end_streak.append(item.find_all('td')[-1].text.strip())
					else:
						i += 9
		if "2011" in link:
			winning_pct.append(" ")
			point_for.append(" ")
			point_against.append(" ")
			end_streak.append(" ")
		else:
			for item in table[0].find_all('tr'):
			# print(len(item.find_all('td')))
				for i in range(len(item.find_all('td'))):
					# print(item.find_all('td')[i].text.strip('\n\n'))
					# print(link[35:-7].replace("_",' '))
					if item.find_all('td')[i].text.strip('\n\n') == link[35:-7].replace("_",' ') \
						or item.find_all('td')[i].text.strip('\n\n')[:-3] == link[35:-7].replace("_",' ') \
						or item.find_all('td')[i].text.strip('\n\n')[3:] == link[35:-7].replace("_",' ') \
						or item.find_all('td')[i].text.strip('\n\n')[4:] == link[35:-7].replace("_",' '):
						winning_pct.append(item.find_all('td')[4].text.strip())
						point_for.append(item.find_all('td')[-3].text.strip())
						point_against.append(item.find_all('td')[-2].text.strip())
						end_streak.append(item.find_all('td')[-1].text.strip())
					else:
						i += 9
	except:
		winning_pct.append(" ")
		point_for.append(" ")
		point_against.append(" ")
		end_streak.append(" ")
		# print the ones that the code are not able to convert, can be manually entered 
		# print(link)
		continue

# remove unrelated item
del winning_pct[3]
del point_for[3]
del point_against[3]
del end_streak[3]
# print(winning_pct)
# print(len(winning_pct))
# print(point_for)
# print(len(point_for))
# print(point_against)
# print(len(point_against))
# print(end_streak)
# print(len(end_streak))
info = []
info.append(winning_pct)
info.append(point_for)
info.append(point_against)
info.append(end_streak)

a = np.array(info)
a_trans = a.transpose()

df = pd.DataFrame(a_trans, columns = ['winnor_season_winning_pct','winnor_season_point_score', \
									'winnor_season_point_allow','winnor_end_streak'])
# print(df.head())
df.to_csv("Winnor_season_stats.csv")






