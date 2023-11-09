from bs4 import BeautifulSoup
import requests
import csv

# URL de la page contenant la liste des articles
base_url = "https://wh40k-fr.lexicanum.com/wiki/"
page_url = "Sp%C3%A9cial:Toutes_les_pages"
url = base_url + page_url

# Obtenir le contenu de la page
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Trouver tous les éléments de la balise ul
article_links = soup.find_all("ul", class_="mw-allpages-chunk")

# Initialiser la liste des titres et des textes
articles = []

# Parcourir tous les éléments de la balise ul
for link in article_links:
    # Trouver tous les liens dans l'élément actuel
    links = link.find_all("a")
    # Parcourir tous les liens trouvés
    for a in links:
        # Obtenir le titre de l'article
        title = a.text.strip()
        # Obtenir l'URL de l'article
        article_url = base_url + a.get("href")
        # Obtenir le contenu de la page de l'article
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.content, "html.parser")
        # Trouver le premier paragraphe avec du texte dans l'élément de classe "mw-parser-output"
        text = ""
        paragraphs = article_soup.select(".mw-parser-output > div > p")
        for p in paragraphs:
            if p.text.strip() != "":
                text = p.text.strip()
                break
        # Ajouter le titre et le texte à la liste correspondante
        articles.append((title, text))
        
# Trouver les liens vers les pages suivantes
next_links = soup.select(".mw-allpages-nav > a")
for link in next_links:
    # Obtenir l'URL de la page suivante
    if link.text == "Page suivante":
        next_url = base_url + link.get("href")
        # Obtenir le contenu de la page suivante
        next_response = requests.get(next_url)
        next_soup = BeautifulSoup(next_response.content, "html.parser")
        # Trouver tous les liens vers des articles dans la page suivante
        next_article_links = next_soup.find_all("ul", class_="mw-allpages-chunk")
        # Parcourir tous les éléments de la balise ul
        for link in next_article_links:
            # Trouver tous les liens dans l'élément actuel
            links = link.find_all("a")
            # Parcourir tous les liens trouvés
            for a in links:
                # Obtenir le titre de l'article
                title = a.text.strip()
                # Obtenir l'URL de l'article
                article_url = base_url + a.get("href")
                # Obtenir le contenu de la page de l'article
                article_response = requests.get(article_url)
                article_soup = BeautifulSoup(article_response.content, "html.parser")
                # Trouver le premier paragraphe avec du texte dans l'élément de classe "mw-parser-output"
                text = ""
                paragraphs = article_soup.select(".mw-parser-output > div > p")
                for p in paragraphs:
                    if p.text.strip() != "":
                        text = p.text.strip()
                        break
                # Ajouter le titre et le texte à la liste correspondante
                articles.append((title, text))
                
