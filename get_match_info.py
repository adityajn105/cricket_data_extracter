"""
Author : Aditya Jain
Contact: https://adityajain.me
"""
from bs4 import BeautifulSoup
import urllib3
import pandas as pd
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def inning(link,inning=1):
    http = urllib3.PoolManager()
    r = http.request('GET',link)
    soup = BeautifulSoup(r.data, 'lxml')
    info = soup.findAll('div',{'class':'cb-mtch-info-itm'})
    title = info[0].find_all('div')[1].text.strip()
    date = info[1].find_all('div')[1].text.strip()
    toss = info[2].find_all('div')[1].text.strip()
    match = soup.findAll("div", {"id": f'innings_{inning}'})[0]
    team = " ".join(match.div.div.span.text.split()[:-1])
    stat = match.findAll( "div", {"class":"cb-ltst-wgt-hdr"} )
    score = " ".join(stat[0].findAll( "span", {"class":'pull-right'} )[0].text.split('\xa0'))
    ###individual batting stats
    filters = lambda x : 'Extras' not in str(x) and 'Did not Bat' not in str(x) and 'Total' not in str(x)
    batsman, outs, runs,balls,fours, sixes = [],[],[],[],[],[]  
    for player in list(filter(lambda x: filters(x), stat[0].findAll('div',{'class':'cb-scrd-itms'}))):
        batsman.append(player.a.text.strip())
        outs.append(player.span.text.strip())
        temp = player.find_all('div')
        i=2
        while not temp[i].text.strip().isnumeric():
            i+=1
        runs.append(temp[i].text.strip())
        balls.append(temp[i+1].text.strip())
        fours.append(temp[i+2].text.strip())
        sixes.append(temp[i+3].text.strip())

    remain = list(filter(lambda x: 'Did not Bat' in str(x), stat[0].findAll('div',{'class':'cb-scrd-itms'})))
    if len(remain)>0:
        for player in remain[0].find_all('a'):
            batsman.append(player.text.strip())
            outs.append('Did not Bat')
            runs.append(0)
            balls.append(0)
            fours.append(0)
            sixes.append(0)
    battingstat = pd.DataFrame( { 'Player':batsman, 'Status':outs,'Runs':runs,
                                       'Balls':balls,'Fours':fours,'Sixes':sixes } )
    ###individual bowling stats
    bowlers,overs,rungiven,wickets,NB,WB,maiden = [],[],[],[],[],[],[]
    for player in stat[1].findAll('div',{'class':'cb-scrd-itms'}):
        bowlers.append(player.a.text.strip())
        divs = player.find_all('div')
        overs.append(divs[1].text.strip() )
        rungiven.append(divs[3].text.strip())
        wickets.append(divs[4].text.strip())
        NB.append(divs[5].text.strip())
        WB.append(divs[6].text.strip())
        maiden.append(divs[2].text.strip())
    bowlingstat = pd.DataFrame({'Player':bowlers,'Overs':overs,'Maiden':maiden,'RunsGiven':rungiven,'Wickets':wickets,
              'NoBall':NB,'WideBall':WB})
    return title, date, toss, team, score, battingstat, bowlingstat