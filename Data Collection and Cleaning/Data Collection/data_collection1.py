import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv

# the goal of the code is to get the temperature data for each super bowl 
# and whether they played indoor or ourdoor

url = "https://www.profootballhof.com/news/super-bowl-game-time-temperatures/"
resp = requests.get(url)
soup = BeautifulSoup(resp.content, "html.parser")
table = soup.find_all("table")

aList = []
pattern = r'\d+°.*'
for member in table[1].find_all("td"):
	# print(member.text)
	match = re.findall(pattern, member.text)
	if match:
		aList.append(match)
# print(aList)
for i in range(len(aList)):
	aList[i] = aList[i][0].strip()
# print(aList)
# print(len(aList))
temp_list = []
for item in aList:
	temp_list.append(item[:2])
# print(temp_list)
envir_list = []
pattern = r'\([a-z]*\)'
for item in aList:
	match = re.findall(pattern, item)
	try:
		envir_list.append(match[0].replace("(","").replace(")",""))
	except:
		envir_list.append("outdoors")
# print(envir_list)

output_list = []
for item in zip(temp_list, envir_list):
	output_list.append(list(item))
# print(output_list)

with open('envir.csv', 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['temperature', 'in/ out'])







