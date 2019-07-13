"""
Author : Aditya Jain
Contact: https://adityajain.me
"""
import pandas as pd
import os
from archive_extract import getAllArchive
from get_matches import getMatches
from get_match_info import inning
import argparse
import shutil
import warnings

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--dir", default="data",help="Enter a directory name")
	parser.add_argument("-y", "--year", required=True, help="Enter a year")

	args = parser.parse_args()
	year = str(args.year)
	main = str(args.dir)

	if not os.path.exists(main): os.mkdir(main)
	if not os.path.exists(os.path.join(main,year)): os.mkdir(os.path.join(main,year))
	archive = getAllArchive(year)
	total = len(archive)
	print(f'Total {total} Tours Found!!')
	styles= ['ODI','T20I']
	i=1
	for link, title in zip(archive.link.values,archive.title.values):
	    df = getMatches(link,title,types=styles)
	    print(f"{i}/{total} || {title} || {len(df)} matches.")
	    i+=1
	    path = os.path.join(main,year,title)
	    if not os.path.exists(path): os.mkdir(path)
	    if not os.path.exists( os.path.join(path,'scorecards') ) : os.mkdir(os.path.join(path,'scorecards'))
	    venues, cstyles, inning1, inning1_score, inning2, inning2_score, results, dates, tosss, scorecard =[],[],[],[],[],[],[],[],[],[]
	    for venue, style, result, link in zip(df.venue,df.type,df.result,df.link):
	        try:
	            title,date, toss, team1, team1_score, bat1_stat, bowl2_stat = inning(link,1)
	            title,date, toss, team2, team2_score, bat2_stat, bowl1_stat = inning(link,2)

	            team1_stat = pd.merge( bat1_stat, bowl1_stat, on='Player', how='outer' )
	            team1_stat['Team'] = team1
	            team2_stat = pd.merge( bat2_stat, bowl2_stat, on='Player', how='outer' )
	            team2_stat['Team'] = team2
	            team1_stat.append(team2_stat,ignore_index=True).fillna(0).to_csv(os.path.join(path,'scorecards',title+'.csv'),index=False)

	            dates.append(date)
	            venues.append(venue)
	            cstyles.append(style)
	            tosss.append(toss)
	            inning1.append(team1)
	            inning2.append(team2)
	            inning1_score.append(team1_score)
	            inning2_score.append(team2_score)
	            results.append(result)
	            scorecard.append(os.path.join(path,'scorecards',title+'.csv'))
	        except Exception as e:
	            warnings.warn("Ignoring an error: "+str(e))
	            pass
	    if len(dates)==0:
	        shutil.rmtree(path)
	    else:
	        pd.DataFrame({"Date":dates,'Venue':venues,'Style':cstyles,'Toss':tosss,'Inning1':inning1,
	                         'Inning2':inning2,'Inning1_Score':inning1_score, 'Inning2_Score':inning2_score, 
	                         'Result':results,'Scorecard':scorecard}).to_csv(os.path.join(path,'tour_stat.csv'),index=False)
