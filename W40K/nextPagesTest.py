from bs4 import BeautifulSoup
import requests
import csv

# URL de la page contenant la liste des articles
url = "https://wh40k-fr.lexicanum.com/wiki/Sp%C3%A9cial:Toutes_les_pages"
url_next = "https://wh40k-fr.lexicanum.com"

# Obtenir le contenu de la page
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# chercher la page suivante et extraire le lien
next_page_div = soup.find("div", class_="mw-allpages-nav").find("a")
next_page_link = url_next + next_page_div["href"]

# initialiser la liste des titres et des textes
titles = []
texts = []

# boucler sur toutes les pages
while True:
    # récuperer le contenu de la page
    response = requests.get(next_page_link)
    soup = BeautifulSoup(response.content, "html.parser")

    # trouver tous les éléments de la balise ul
    article_links = soup.find_all("ul", class_="mw-allpages-chunk")

    # parcourir tous les éléments de la balise ul
    for link in article_links:
        # Trouver tous les liens dans l'élément actuel
        links = link.find_all("a")
        # Parcourir tous les liens trouvés
        for a in links:
            # Obtenir le titre de l'article
            title = a.text.strip()
            # Obtenir l'URL de l'article
            article_url = "https://wh40k-fr.lexicanum.com" + a.get("href")
            # Obtenir le contenu de la page de l'article
            article_response = requests.get(article_url)
            article_soup = BeautifulSoup(article_response.content, "html.parser")
            # Trouver le premier paragraphe contenant du texte dans l'élément de classe "mw-parser-output"
            paragraphs = article_soup.find("div", class_="mw-parser-output").find_all("p")
            for p in paragraphs:
                if p.text.strip():
                    text = p.text.strip()
                    break
            # Ajouter le titre et le texte à la liste correspondante
            titles.append(title)
            texts.append(text)

    # chercher la page suivante ou arrêter la boucle si on est arrivé à la dernière page
    next_page_div = soup.find("div", class_="mw-allpages-nav")
    if not next_page_div:
        break
    next_page_link = "https://wh40k-fr.lexicanum.com" + next_page_div.find("a", text="suivant")["href"]

# Ajouter le titre et le texte à la fin du fichier correspondant
with open("article_data.csv", "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(titles)):
        writer.writerow([titles[i], texts[i]])