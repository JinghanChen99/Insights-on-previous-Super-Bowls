import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv
import pandas as pd
import numpy as np

# the goal of this code is to get the average viewers/ total viewers, TV ratings,
# and average cost per 30 seconds of ads
url = 'https://en.wikipedia.org/wiki/Super_Bowl_television_ratings'
resp = requests.get(url)
soup = BeautifulSoup(resp.content, 'html.parser')
table = soup.find_all('table', attrs = {'class':'wikitable'})
# get the necessary data for super bowl I separately from other super bowls since it was 
# boardcast by two networks
row = []
table_data = []
for item in table[0].find_all('tr')[2:4]:
	# print(item.text)
	row.append(item.text.strip())
# print(row)
for i in range(len(row)):
	row[i] = row[i].split('\n\n')
row[0][5] = row[0][5][:len(row[0][5])-4].replace(',','')
CBS_avg_viewers = int(row[0][5])
# print(CBS_avg_viewers)
row[0][6] = row[0][6][:len(row[0][6])-4].replace(',','')
CBS_tot_viewers = int(row[0][6])
# print(CBS_tot_viewers)
row[0][8] = row[0][8][:len(row[0][8])-4]
CBS_TV_ratings = float(row[0][8])
# print(CBS_TV_ratings)
row[0][9] = row[0][9][:len(row[0][9])-4]
CBS_TV_share = float(row[0][9])
# print(CBS_TV_share)
row[0][-1] = row[0][-1][:len(row[0][-1])-4].replace(',','')
CBS_ads_cost = int(row[0][-1][1:])
# print(CBS_ads_cost)

row[1][1] = row[1][1][:len(row[1][1])-4].replace(',','')
NBC_avg_viewers = int(row[1][1])
# print(NBC_avg_viewers)
row[1][2] = row[1][2][:len(row[1][2])-4].replace(',','')
NBC_tot_viewers = int(row[1][2])
# print(NBC_tot_viewers)
row[1][4] = row[1][4][:len(row[1][4])-4]
NBC_TV_ratings = float(row[0][9])
# print(CBS_TV_ratings)
row[1][5] = row[1][5][:len(row[1][5])-4]
NBC_TV_share = float(row[1][5])
# print(CBS_TV_share)
row[1][-1] = row[1][-1][:len(row[1][-1])-4].replace(',','')
NBC_ads_cost = int(row[1][-1][1:])
# print(NBC_ads_cost)

avg_viewers = []
tot_viewers = []
TV_rating = []
TV_share = []
ads_cost = []
avg_viewers.append(round((CBS_avg_viewers+NBC_avg_viewers)/2, 0))
tot_viewers.append(round((CBS_tot_viewers+NBC_tot_viewers)/2, 0))
TV_rating.append(round((CBS_TV_ratings+NBC_TV_ratings)/2, 0))
TV_share.append(round((CBS_TV_share+NBC_TV_share)/2, 0))
ads_cost.append(round((CBS_ads_cost+NBC_ads_cost)/2, 0))
# print(avg_viewers)
# print(tot_viewers)
# print(TV_rating)
# print(TV_share)
# print(ads_cost)
row_str = []
tableData = []
row_str = [item.text for item in table[0].find_all('tr')[4:]]
for i in range(len(row_str)):
	row_str[i] = row_str[i].split('\n\n')
# print(row_str)
for item in row_str:
	avg_viewers.append(item[5])
	tot_viewers.append(item[6])
	TV_rating.append(item[8])
	TV_share.append(item[9])
	ads_cost.append(item[-1])
# print(avg_viewers)
# print(tot_viewers)
# print(TV_rating)
# print(TV_share)
# print(ads_cost)
table_data.append(avg_viewers)
table_data.append(tot_viewers)
table_data.append(TV_rating)
table_data.append(TV_share)
table_data.append(ads_cost)
# print(table_data)

# table_data now contains 5 columns of data, now I started the process of data cleaning
for i in range(len(table_data)):
	if i == 0:
		for j in range(len(table_data[i])):
			try:
				table_data[i][j] = int(table_data[i][j][:len(table_data[i][j])-4].replace(',',''))
			except:
				continue
	elif i == 1:
		for j in range(len(table_data[i])):
			try:
				table_data[i][j] = int(table_data[i][j][:len(table_data[i][j])-4].replace(',',''))
			except:
				if table_data[i][j] == 'Unknown':
					table_data[i][j] = 0
				continue
	elif i == 2:
		for j in range(len(table_data[i])):
			try:
				table_data[i][j] = float(table_data[i][j][:len(table_data[i][j])-4])
			except:
				continue
	elif i == 3:
		for j in range(len(table_data[i])):
			try:
				table_data[i][j] = float(table_data[i][j][:len(table_data[i][j])-4])
			except:
				continue
	elif i == 4:
		for j in range(len(table_data[i])):
			try:
				table_data[i][j] = table_data[i][j].strip()
				table_data[i][j] = int(table_data[i][j][1:len(table_data[i][j])-4].replace(',',''))
			except:
				# print(table_data[i][j])
				if j == len(table_data[i]) -1:
					table_data[i][j] = int(table_data[i][j][2:len(table_data[i][j])-4].replace(',',''))
				continue
# print(table_data)

a = np.array(table_data)
# print(a)
a_trans = a.transpose()
# print(a_trans)
df = pd.DataFrame(a_trans, columns=['Average Viewers','Total Viewers','TV_rating', \
										'TV_share','30-sec Ads cost'])
# print(df)
# print(df.shape)
df.to_csv("viewers_Ads_data.csv")
