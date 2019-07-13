"""
Author : Aditya Jain
Contact: https://adityajain.me
"""
from bs4 import BeautifulSoup
import urllib3
import pandas as pd
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getMatches(link,title,types=['ODI','T20I']):
    """
        link : series link
        title: title of series
        types: 'list to filter match'
    """
    http = urllib3.PoolManager()
    r = http.request('GET', link)
    soup = BeautifulSoup(r.data, 'lxml')
    match = soup.findAll("div", {"class": 'cb-srs-mtchs-tm'})
    results,venue,links,typ = [],[],[],[]
    for m in match:
        try:
            #if m.span.text.strip().split()[-1].strip() in types:
            results.append(m.find_all('a')[1].text.strip())
            venue.append(m.div.text.strip())
            typ.append(m.span.text.strip().split()[-1].strip())
            links.append('https://www.cricbuzz.com/live-cricket-scorecard/'+"/".join(m.a['href'].split('/')[2:]))
        except:
            pass
    return pd.DataFrame( {'title':title,'result':results, 'venue':venue, 'link':links, 'type':typ } )