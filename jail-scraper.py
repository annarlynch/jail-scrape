

import requests
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd

def scrape():
    url = 'http://209.152.119.10/vine/currentinmates/currentinmates.html'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    rows = soup.find_all('tr')
    prisoner_rows = rows[1:]
    ar = np.array(prisoner_rows)
    prisoner_chunks = np.split(ar, len(prisoner_rows) / 6)

    def chunkdict(chunk):
        output = {}
        output["pic"] = chunk[0].find_all("img")[0]["src"]
        output["name"] = chunk[0].find_all("td")[-1].text
        output["age"] = chunk[1].find_all("td")[-1].text
        output["gender"] = chunk[2].find_all("td")[-1].text
        output["detained"] = chunk[3].find_all("td")[-1].text
        output["released"] = chunk[4].find_all("td")[-1].text
        output["charges"] = chunk[5].find_all("td")[-1].text
        return output
    prisoner_dicts = [chunkdict(x) for x in prisoner_chunks]
    df = pd.DataFrame(prisoner_dicts)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    df = df[['name', 'gender', 'age', 'detained', 'charges', 'released', 'pic']]
    df_filtered = df[df['charges'].str.contains('ICE ', na = False)]
    df_filtered.insert(loc=0, column='Row Number', value=np.arange(len(df_filtered)))

    return(df_filtered)
    
    scrape()
