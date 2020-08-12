########## This file will contain all the main functions and helper functions you utilized for each analysis ##########
import pandas as pd
import numpy as np

def general_info(data):
	"""
		This functions provides general information about the history of Super Bowls. It answers three basic
		questions: 
		1. What are the top five stadiums that hosted the most number of Super Bowls? And what was the average 
		point difference for these top five stadiums?
		2. Who are the top 5 QBs that have won the most super bowls? And what was the average point 
		difference for their wins?
		3. Who did the most Super Bowl winning QB played against? Who is the MVP in those Super Bowls? 
		And where did he won those Super Bowls?
		All of the data for this specific analysis comes from the SuperBowl_base_update.csv
		Parameters:
		data (file): a csv file that contains the dataset for this analysis

		Returns:
		a tuple contains three dataframes corresponding to the three questions
	"""
	df = pd.read_csv(data)
	info_df = df[['SB', 'Attendance', 'QB  Winner', 'Coach Winner', 'Winner', 'Loser', 'MVP', \
		'Stadium', 'City', 'State', 'Point Difference']]
	# which stadium hosted the most number of super bowls
	host = info_df.groupby(['Stadium', 'City', 'State'])['Point Difference'].agg(['count', \
		'mean']).sort_values(by='count', ascending=False).head()
	host.columns = ['Number of SB hosted', 'Average Point Difference']
	# who won the most super bowls and what's the point difference for their wins
	winning_QBs = info_df.groupby('QB  Winner')['Point Difference'].agg(['count', \
		'mean']).sort_values(by='count', \
		ascending=False).head()
	winning_QBs.columns = ['Number of SB wins','Average Point Difference']
	# info about most winning QB
	the_goat = info_df[info_df['QB  Winner']=='Tom Brady'][['SB','Coach Winner','Loser','MVP',\
		'Stadium','City','State']].set_index('SB')
	return host, winning_QBs, the_goat


def playing_environment(data):
	"""
		This functions is trying to investigate whether indoor or outdoor has an influence on 
		the point difference or the number of attendees and whether temperature has some impact on the point 
		difference or the number of attendees.
		Temperaure was converted to a categorical variable. 
		Data for 'temperature' and 'in/ out' were scraped from the web.
		Parameters:
		data (file): a csv file that contains the dataset for this analysis

		Returns:
		a dateframe with columns of number of Attendance and Point Difference and index of indoor and outdoor
	"""
	df = pd.read_csv(data)
	df2 = df[['SB', 'Attendance', 'Point Difference', 'temperature',
       'in/ out']]
	df2['Temp_group'] = pd.cut(df2.temperature,
                     bins=[0, 50, 65, 75, 85],
                     labels=["Freezing", "Cold", "Comfortable", "Hot"])
	envir_vs_performance = df2.groupby(['in/ out','Temp_group'])[['Attendance', 'Point Difference']].mean()
	envir_vs_performance.fillna("No data in this category")
	return envir_vs_performance


def rating_vs_competitiveness(data):
	"""
		This functions is trying to investigate whether the competitiveness of the game (calculated by the 
		average point difference for every quarter) has the influence on the television ratings. 
		competitive_score was converted to a categorical variable. 
		Data for 'Average Viewers', 'Total Viewers', 'TV_rating', 'TV_share' were scraped from the web.
		Parameters:
		data (file): a csv file that contains the dataset for this analysis

		Returns:
		a dateframe with columns of TV_rating and TV_share and index of different competitive levels
	"""
	df = pd.read_csv(data)
	# competitive_score was calculated in the data collection process (data_collection2.py)
	df3 = df[['SB', 'Point Difference', 'Average Viewers', 'Total Viewers', 'TV_rating', 'TV_share','competitive_score']]
	df3['comp_group'] = pd.cut(df3.competitive_score,
                     bins=[0, 4.5, 6, 10, 13],
                     labels=["Highly Competitive", "Competitive", "Not Competitive", "No match"])
	TV_rating_vs_competitiveness = df3.groupby('comp_group')[['TV_rating','TV_share']].mean()
	return TV_rating_vs_competitiveness

def TV_rating_vs_ads_cost(data):
	"""
		This functions is trying to investigate the strength of the correlation between TV ratings ('Average 
		Viewers', 'Total Viewers', 'TV_rating', 'TV_share') and '30-sec Ads cost'.
		Data for 'Average Viewers', 'Total Viewers', 'TV_rating', 'TV_share', '30-sec Ads cost' were scraped 
		from the web.
		Parameters:
		data (file): a csv file that contains the dataset for this analysis

		Returns:
		a tuple with the highest correlation and its corresponding variable
	"""
	df = pd.read_csv(data)
	df4 = df[['SB', 'Average Viewers', 'Total Viewers', 'TV_rating', 'TV_share', '30-sec Ads cost']]
	aList = []
	for item in list(df4)[1:-1]:
		aList.append(["30-sec Ads cost and " + item, df4['30-sec Ads cost'].corr(df4[item])])
	corr = 0
	variable = ''
	for member in aList:
		if member[1] > corr:
			corr = member[1]
			variable = member[0]
	return variable, round(corr, 3)

def season_stats_comparison(data):
	"""
		This functions is trying to investigate the difference between the the winning team’s season 
		performance and the losing team's season performance. 
		I selected season winning percentage, end of the season streak, points scored, and points against to
		be the parameters for this analysis.  
		Data for 'winnor_season_winning_pct', 'winnor_season_point_score', 'winnor_season_point_allow', 
		'winnor_end_streak', 'loser_season_winning_pct', 'loser_season_point_score', 'loser_season_point_allow'
		'loser_end_streak' were scraped from the web.
		'Winning_streak', 'Losing_streak', 'Winning_streak.1', 'Losing_streak.1' were generated from the c
		corresponding columns of 'winnor_end_streak' and 'loser_end_streak'.
		Parameters:
		data (file): a csv file that contains the dataset for this analysis

		Returns:
		a dataframe with index of Point Score, Point Allow, Winning Streak, and Losing Streak 
		and columns of Winner and loser
	"""
	df = pd.read_csv(data)
	df5 = df[['SB', 'winnor_season_winning_pct', 'winnor_season_point_score', 'winnor_season_point_allow', \
		'Winning_streak', 'Losing_streak', 'loser_season_winning_pct', 'loser_season_point_score', \
		'loser_season_point_allow', 'Winning_streak.1', 'Losing_streak.1']]
	df5.loc['Average'] = [np.nan, df5['winnor_season_winning_pct'].mean(),df5['winnor_season_point_score'].mean(),\
					df5['winnor_season_point_allow'].mean(),\
					df5['Winning_streak'].mean(),df5['Losing_streak'].mean(),df5['loser_season_winning_pct'].mean(),\
					df5['loser_season_point_score'].mean(),\
					df5['loser_season_point_allow'].mean(),\
					df5['Winning_streak.1'].mean(), df5['Losing_streak.1'].mean()]
	df5.tail(1).transpose()
	winner_season_stats = df5.tail(1).transpose().iloc[1:6,:]
	winner_season_stats.reset_index(inplace=True)
	loser_season_stats = df5.tail(1).transpose().iloc[6:,:]
	loser_season_stats.reset_index(inplace=True)
	df6=pd.concat([winner_season_stats, loser_season_stats],axis=1)
	df6.set_index(pd.Index(['Winning pct','Point Score','Point Allow', 'Winning Streak','Losing Streak']), inplace=True)
	df7 = df6.loc[:, 'Average']
	df7.columns = ['Winner','Loser']
	return df7

if __name__ == '__main__':
	# general_info
	host, winning_QBs, the_goat = general_info('final_dataset.csv')
	print('The top five stadiums that hosted the most number of Super Bowls are: \n')
	print(host)
	print('The QBs who won the most super bowls and the average point difference for their wins: \n')
	print(winning_QBs)
	print('Who did the most Super Bowl winning QB played against? Who is the MVP? And where did he won it? \n')
	print(the_goat)
	print('\n')

	# playing_environment
	print("Does temperature and indoor or outdoor have a impact on the point difference and number of attendance?")
	print(playing_environment('final_dataset.csv'))
	print("The result of this function shows that the game is more competitive when it was played outdoor in comfortable weather.")
	print('\n')

	# TV_rating_vs_competitiveness
	print("Does the competitiveness of the game influence the TV_ratings?")
	print(rating_vs_competitiveness('final_dataset.csv'))
	print("The result of this function shows that the competitiveness of the game does not influence the TV_ratings.")
	print('\n')

	# TV_rating_vs_ads_cost
	print("Which variable has the strongest correlation with the cost of 30-second ads? ")
	variable, corr = TV_rating_vs_ads_cost('final_dataset.csv')
	print(variable + " has the strongest strength of linear relationship with the cost of 30-second ads with the correlation of " + str(corr))
	print("This makes sense because marketers are more willingly to pay more to reach average viewers.")
	print('\n')

	# season_stats_comparison
	print("What are some difference between the season statistics of the winning and losing teams?")
	print(season_stats_comparison('final_dataset.csv'))
	a = """The result of this function shows that winning and losing teams have relatively the same winning
percentage and offense throughout the season, but winning teams have significantly better defense.
Also, the winner of the Super Bowl seems to have longer winning streak at the end of the regular season 
going into the playoffs. Losing teams tend to have a losing streaks at the end of the regular season.
"""
	print(a)




