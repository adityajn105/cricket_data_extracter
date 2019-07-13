"""
Author : Aditya Jain
Contact: https://adityajain.me
"""
from bs4 import BeautifulSoup
import urllib3
import pandas as pd
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getAllArchive(year):
    http = urllib3.PoolManager()
    link = f"https://www.cricbuzz.com/cricket-scorecard-archives/{year}"
    r = http.request('GET', link)
    soup = BeautifulSoup(r.data, 'lxml')
    archive = soup.findAll("div", {"class": 'cb-srs-lst-itm '})
    title = list( map( lambda x: x.a['title'].strip(), archive) )
    link = list( map( lambda x: 'https://www.cricbuzz.com'+x.a['href'], archive) )
    return pd.DataFrame( { 'title':title, 'link':link } )

if __name__ == '__main__':
	year = input("Please Enter a Year")
	print(getAllArchive(year))