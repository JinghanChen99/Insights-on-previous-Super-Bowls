import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv
import pandas as pd
import numpy as np

# The goal of this code is to get losing team season stats 
# and combine with the winning team season stats to see if there is a shared features for the winning team
# I noticed that the table I want to get the data from has different style and different position in
# each losing team's link. As a result, I had a hard time getting all the data I want through program
# This program helps me to get every line of data I want except 10 lines out of 54.
# I have to manually enter data for those 10 lines.
with open('losing_links.csv', 'r') as file:
	reader = csv.reader(file)
	readerList = [line[1] for line in reader]
# print(readerList)
# fix the one of the links
# for link in readerList:
# 	if 'Louis_Rams_season' in link:
# 		link = 'https://en.wikipedia.org/wiki/2001_St._Louis_Rams_season'
readerList = readerList[1:]
winning_pct = []
point_for = []
point_against = []
end_streak = []
for link in readerList:
	# print(link)
	if 'Louis_Rams_season' in link:
		link = 'https://en.wikipedia.org/wiki/2001_St._Louis_Rams_season'
	resp = requests.get(link)
	soup = BeautifulSoup(resp.content, "html.parser")
	if len(winning_pct) <= 9:
		if len(winning_pct) == 4 or len(winning_pct) == 6:
			table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size: 95%; text-align:center'})
		table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size:95%; text-align:center'})
	elif len(winning_pct) >= 10 and len(winning_pct) <= 15:
		table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size: 95%;'})
	elif len(winning_pct) >= 16 and len(winning_pct) <= 19:
		table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size: 95%; text-align:center'})
	elif len(winning_pct) >= 20 and len(winning_pct) <= 24:
		if len(winning_pct) == 22:
			table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size: 95%; text-align:center'})
		table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size:95%; text-align:center'})
	elif len(winning_pct) >= 25 and len(winning_pct) <= 52:
		if len(winning_pct) == 28:
			table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size:95%; text-align:center'})
		elif len(winning_pct) == 31 or len(winning_pct) == 47 or len(winning_pct) == 52:
			table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size: 95%; text-align:center'})
		table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size: 95%;'})
	elif len(winning_pct) == 53:
		table = soup.find_all("table", attrs={'class':'wikitable', 'style':'font-size:95%; text-align:center'})
	try:
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
# print(winning_pct)
# print(point_for)
# print(point_against)
# print(end_streak)

# print(len(winning_pct))
# The length is 53 
# for some reason, the 2010 Steelers' record was not recorded
# I used python here to insert the corresponding value
winning_pct.insert(44, '.750')
point_for.insert(44, '375')
point_against.insert(44, '232')
end_streak.insert(44, 'W2')

# print(winning_pct)
# print(len(winning_pct))

info = []
info.append(winning_pct)
info.append(point_for)
info.append(point_against)
info.append(end_streak)

a = np.array(info)
a_trans = a.transpose()

df = pd.DataFrame(a_trans, columns = ['loser_season_winning_pct','loser_season_point_score', \
									'loser_season_point_allow','loser_end_streak'])
# print(df.head())
df.to_csv("loser_season_stats.csv")


