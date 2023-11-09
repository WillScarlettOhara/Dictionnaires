import requests
from bs4 import BeautifulSoup
import csv

url='https://wh40k-fr.lexicanum.com/wiki/Sp%C3%A9cial:Toutes_les_pages?from=&to=&namespace=0&hideredirects=1'

# initialiser la liste des titres et des textes
titles = []
texts = []

while url:
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    ul=soup.find('ul',class_='mw-allpages-chunk')
    a=ul.find_all('a')
    # Parcourir tous les liens trouvés
    for link in a:
        # Obtenir l'URL de l'article
        article_url = "https://wh40k-fr.lexicanum.com" + link.get("href")
        # Obtenir le contenu de la page de l'article
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.content, "html.parser")
        
        # Trouver le premier paragraphe avec du texte dans l'élément de classe "mw-parser-output" et qui n'est pas dans un tag "table"
        contenu = ""
        div = article_soup.find("div", class_="mw-parser-output")
        paragraphs = div.find_all("p")
        for p in paragraphs:
            if p.text.strip() and p.parent.name != "table" and p.parent.name != "tr" and p.parent.name != "tbody" and p.parent.name != "td":
                contenu = p.text.strip()
                break

        # Find the unordered list
        ul = div.find("ul")
        if ul and ul.find_previous_sibling() == p: # Only get the ul and li tags if they are right after the first p tag
            contenu = contenu + "<ul>"
            for li in ul.find_all('li'):
                contenu += "<li>"+li.text + "</li> "
            contenu = contenu[:-1] + "</ul>" # remove the last space

        # Ajouter le titre et le texte à la liste correspondante
        if len(contenu.strip()) > 3:
            titles.append(link.text)
            texts.append(contenu)


    div=soup.find('div',class_='mw-allpages-nav')
    a=div.find_all('a')
    for link in a:
        if 'suivante' in link.text:
            url='https://wh40k-fr.lexicanum.com'+link.get('href')
            break
        else:
            url=None

# Ajouter le titre et le texte à la fin du fichier correspondant
with open("scraped_pages.txt", "w", newline="", encoding="utf-8") as tabfile:
    for i in range(len(titles)):
        tabfile.write(titles[i] + "\t" + texts[i].replace("\n","") + "\n")