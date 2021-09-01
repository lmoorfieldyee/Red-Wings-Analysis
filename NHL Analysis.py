import numpy as np
import pandas as pd
import requests
import matplotlib as plt
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver

#initialize chrome driver
PATH = '/Users/Liam/Desktop/chromedriver'
driver = webdriver.Chrome(PATH)

#extracting data xml data from website
driver.get("https://www.hockey-reference.com/teams/DET/2021.html#all_team_stats")
soup_file=driver.page_source
soup = BeautifulSoup(soup_file, 'lxml')

#scraping relevant information from dataset
table = soup.find('table', id="team_stats")
table_rows = table.find_all('tr')
table_headers = []
for header in table.find_all('th'):
    table_headers.append(header.text)
table_headers = table_headers[1:28]
table_headers.append('year')

#creating dataframe
nhl_df = pd.DataFrame(columns = table_headers)

years = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010,
         2009, 2008, 2007, 2006, 2004, 2003, 2002, 2001, 2000, 1999]

html_start = 'https://www.hockey-reference.com/teams/DET/'
html_end = '.html#all_team_stats'

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    row.append(2021)
    if len(row)==28:
        append_len = len(nhl_df)
        nhl_df.loc[append_len] = row


for i in years:
    new_row = []
    i = str(i)
    url = str(html_start+i+html_end)
    driver.get(url)
    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file, 'lxml')
    table = soup.find('table', id="team_stats")
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        new_row = [i.text for i in td]
        new_row.append(i)
        if len(new_row)==28:
            append_len = len(nhl_df)
            nhl_df.loc[append_len] = new_row
            print(i)

nhl_df = nhl_df[['GP', 'W', 'L', 'OL', 'PTS', 'PTS%', 'GF', 'GA', 'SRS', 'SOS',
       'GF/G', 'GA/G', 'PP', 'PPO', 'PP%', 'PPA', 'PPOA', 'PK%', 'SH', 'SHA',
       'S', 'S%', 'SA', 'SV%', 'PDO', 'SO', 'year']]

remaining_years = [1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990]

for i in remaining_years:
    new_row = []
    i = str(i)
    url = str(html_start+i+html_end)
    driver.get(url)
    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file, 'lxml')
    table = soup.find('table', id="team_stats")
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        new_row = [i.text for i in td]
        new_row.append(i)
        if len(new_row)==27:
            append_len = len(nhl_df)
            nhl_df.loc[append_len] = new_row
            print(i)

nhl_df.to_csv()

#data frame scrapped includes Red Wings Data and league average for the year.
#I am subsetting out only the relevant information pertaining to the detroit red wings
rows = []
for i in range(0,52):
    if i % 2 ==0:
        rows.append(i)

red_wings = nhl_df.iloc[rows]

#converting year to to_datetime
red_wings['year'] = pd.to_datetime(red_wings['year'], format='%Y').dt.year

#sorting data based on year
red_wings = red_wings.sort_values(by='year', ascending=True)

red_wings_graph = red_wings[['PTS%', 'SV%', 'year']]
red_wings_graph.set_index('year')
red_wings_graph.rename(columns={'PTS%':'win_percent', 'SV%':'save_percent'}, inplace=True)

year = red_wings_graph['year']
win_percent = red_wings_graph['win_percent']
save_percent = red_wings_graph['save_percent']


save_win_corr = red_wings_graph['win_percent'].corr(red_wings_graph['save_percent'])


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()


ax1.plot(year, win_percent, '-', color='blue', label='Win Percent')
ax2.plot(year, save_percent, '-', color='red', label='Save Percent')

ax1.set_xlabel('NHL Season')
ax1.set_ylabel('Win Percent')
ax2.set_ylabel('Save Percent')
ax1.legend(loc=2)
ax2.legend(loc=1)
plt.title('Red Wings Win & Save \n Percentage by season')

#new comment
