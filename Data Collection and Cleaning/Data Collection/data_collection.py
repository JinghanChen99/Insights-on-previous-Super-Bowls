import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv

# scrap necessary information from the web to complete the base databset 
# by adding the lateset two super bowls 
root_url = 'https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions'
resp = requests.get(root_url)
soup = BeautifulSoup(resp.content, "html.parser")
table = soup.find_all("table")
# pprint(table[1])
super_bowl_links = table[1].find_all('a')
# print(super_bowl_links)
links = [super_bowl.get("href") for super_bowl in super_bowl_links]

# get some info from base table 
info = []
each = []
for datapoint in table[1].find_all('td'):
	each.append(datapoint.text.strip())
	if len(each) == 9:
		info.append(each)
		each = []
# print(info)
need_info = []
for super_bowl in info:
	if super_bowl[0] == "LIII" or super_bowl[0] == "LIV":
		need_info.append(super_bowl)
# print(need_info)

pattern = r"[0-9]*"
for item in need_info:
	aList= []
	match1 = re.findall(pattern, item[3])
	for member in match1:
		if len(member) != 0:
			aList.append(member)
	item[3] = aList
# print(need_info)

# hrefs contains all sublinks to each super bowl
hrefs=[]
pattern = r'\/wiki\/Super_Bowl_.*'
for href in links:
	match = re.findall(pattern, href)
	# print(match)
	if len(match) != 0:
		hrefs.append(match[0])
# print(hrefs)

# find more info to complete the table 
latest_two_sublinks = [] 
for href in hrefs:
	if "LIII" in href:
		latest_two_sublinks.append(href)
	elif "LIV" in href:
		latest_two_sublinks.append(href)
	else:
		continue
latest_two_sublinks = latest_two_sublinks[2:]
# print(latest_two_sublinks)
info = []
for sublink in latest_two_sublinks:
	url = 'https://en.wikipedia.org' + sublink
	# print(url)
	resp = requests.get(url)
	soup = BeautifulSoup(resp.content, "html.parser")
	table = soup.find_all("table", attrs = {'class':'infobox vevent'})
	each = []
	count = 0
	for item in table[0].find_all("a"):
		each.append(item.text)
		if len(each) == 48:
			info.append(each)
			each = []
# print(info)
winning_coach = []
losing_coach = []
MVP = []
for item in info:
	MVP.append(item[10])
	winning_coach.append(item[5])
	losing_coach.append(item[6])
# When checking the result, super bowl LIII winning coach and losing coach are flipped
# have to flipping them back
# print(winning_coach)
# print(losing_coach)
temp = winning_coach[1]
winning_coach[1] = losing_coach[1]
losing_coach[1] = temp
# print(MVP)

# find QB from both team
new_info = []
for sublink in latest_two_sublinks:
	url = 'https://en.wikipedia.org' + sublink
	# print(url)
	resp = requests.get(url)
	soup = BeautifulSoup(resp.content, "html.parser")
	table = soup.find_all("table", attrs = {'class':'wikitable'})
	comparison_list = []
	comparison = []
	for item in table[7].find_all("a")[1:]:
		comparison.append(item.text)
		if len(comparison) == 2:
			comparison_list.append(comparison)
			comparison = []
	new_info.append(comparison_list)
	comparison_list = []
# pprint(new_info)
QBs = []
for i in new_info:
	QBs.append(i[8])
# print(QBs)

# final clean up process to add all information needed to complete the base table
winningQB = []
losingQB = []
winningQB.append(QBs[0][0])
winningQB.append(QBs[1][1])
losingQB.append(QBs[0][1])
losingQB.append(QBs[1][0])
# print(winningQB)
# print(losingQB)
# print(winning_coach)
# print(losing_coach)
# print(MVP)
info_list = []
for i in need_info:
	for j in range(2):
		value_list = [i[1], i[0], i[-2], winningQB[j], winning_coach[j], i[2], i[3][0], \
					losingQB[j], losing_coach[j], i[4], i[3][1], MVP[j], i[-4], i[-3]]
		info_list.append(value_list)
# according to the result, only the first and the last iteration of the code provides correct information
result = []
result.append(info_list[0])
result.append(info_list[-1])
# print(result)

# data cleaning process, make the added information the same format as the base dataset
pattern = r'([A-Z]\(\d*, \d*.\d*\))'
for item in result:
	match1 = re.search(pattern, item[5])
	start1 = match1.start()
	item[5] = item[5][:start1]

	match2 = re.search(pattern, item[-5])
	start2 = match2.start()
	item[-5] = item[-5][:start2]
# print(result)
pattern = r'\(\d*.*'
for item in result:
	match1 = re.search(pattern, item[-1])
	start1 = match1.start()
	item[-1] = item[-1][:start1].strip()

	match2 = re.search(pattern, item[-2])
	if match2 == None:
		continue
	else:
		start2 = match2.start()
	item[-2] = item[-2][:start2].strip()

for item in result:
	for member in item[-1].split(','):
		item.append(member.strip())
	item.append(int(item[6])-int(item[10]))
	del item[-4]
# print(result)
# write data to the existing file 
with open('SuperBowl_base_update.csv', "a") as file:
	csv_writer = csv.writer(file)
	csv_writer.writerow('\n')
	csv_writer.writerows(result)









