# 1. Scrape this website:  https://wh40k-fr.lexicanum.com/wiki/Sp%C3%A9cial:Toutes_les_pages?from=&to=&namespace=0&hideredirects=1  with python and Beautiful Soup
# 2. Locate the element with tag "ul" and class "mw-allpages-chunk". Scrape all the "a" elements inside.
# 3. Get the text attribute and place it in the first column of a data frame.
#4. Locate the next page with tag "div"and class "mw-allpages-nav". Scrape all the "a" elements inside.
#5. Get the text attribute and select the one that has the word "suivant" somewhere.
#6. Get the "href" and add it to the url "https://wh40k-fr.lexicanum.com" to optain the new website to scrape.
#7. Repeat step 2 and 3 with new this new url until there is no more "suivant"
#7. add results in a csv file

#Answer

import requests
from bs4 import BeautifulSoup
import pandas as pd

url='https://wh40k-fr.lexicanum.com/wiki/Sp%C3%A9cial:Toutes_les_pages?from=&to=&namespace=0&hideredirects=1'

data=[]
while url:
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    ul=soup.find('ul',class_='mw-allpages-chunk')
    a=ul.find_all('a')
    for link in a:
        data.append(link.text)
    div=soup.find('div',class_='mw-allpages-nav')
    a=div.find_all('a')
    for link in a:
        if 'suivante' in link.text:
            url='https://wh40k-fr.lexicanum.com/'+link.get('href')
            break
        else:
            url=None

df=pd.DataFrame(data,columns=['Page Name'])
df.to_csv('scraped_pages.csv',index=False)