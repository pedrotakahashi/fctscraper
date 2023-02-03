import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import simpledialog
from scraper import Scraper
from log import logger
import codecs
import datetime
import sys

URL, KEYWORD = "", ""
root = tk.Tk()
root.withdraw()


def crawl_from_url():
    seen_texts = set()
    matches = []
    scraper = Scraper(url=URL)

    all_pages_links_from_website = scraper.get_all_pages_of_website()

    for page_link in all_pages_links_from_website:
        if type(page_link) is not str:
            break
        logger.debug(f"Scraping page: {page_link}")
        try:
            soup = scraper.scrap_url(page_link)
            scraper.set_soup(soup)
            # Encontra todas as tags HTML que contêm o texto da palavra-chave
            page_matches = soup.find_all(text=lambda text: KEYWORD in text)
            for match in page_matches:
                if match not in seen_texts:
                    matches.append(match)
                    seen_texts.add(match)
        except Exception as e:
            logger.error(f"Error scraping page: {page_link}")
            logger.error(e)

    now = datetime.datetime.now()
    date_scraped = now.strftime("%Y-%m-%d %H-%M-%S")
    # Escreve os textos encontrados em um arquivo .txt
    with codecs.open(f"resultados_{date_scraped}.txt", "w", "utf-8") as f:
        f.write(f"URL da página raspada: {URL}\n")
        f.write(f"Data da raspagem: {date_scraped}\n")
        f.write(f"Quantidade de páginas raspadas: {len(all_pages_links_from_website)}\n")
        for match in matches:
            f.write(match + "\n")

    # Escreve os textos encontrados em uma planilha xls
    with open(f"resultados_{date_scraped}.csv", mode="w",newline='', encoding="utf-8") as csv_file:
        fieldnames = ["palavra-chave", "textos", "URL da página", "Data da raspagem", "Quantidade de páginas raspadas"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for match in matches:
            writer.writerow({"palavra-chave": KEYWORD, "textos": match, "URL da página": URL, "Data da raspagem": date_scraped, "Quantidade de páginas raspadas": len(all_pages_links_from_website)})

    close = simpledialog.askstring(
            "Nova Busca", "Deseja realizar uma nova busca? (s/n)", parent=root)
    if close.upper() != "S":
        sys.exit()



def gui():
    global URL, KEYWORD
    while True:
    # URL do site a ser rastreado
        URL = simpledialog.askstring("Palavra Chave", "Insira site", parent=root)
        # Palavra-chave a ser procurada
        KEYWORD = simpledialog.askstring(
        "Palavra Chave", "Insira Palavra chave", parent=root)
        # Realiza a busca
        crawl_from_url()
        
         # Pergunta se o usuário deseja realizar uma nova busca
        result = simpledialog.askstring(
            "Nova Busca", "Deseja realizar uma nova busca? (s/n)", parent=root
        )
        if result.lower() != "s":
            break

    print("Sistema encerrado.")

def main():
    gui()
    crawl_from_url()


if __name__ == "__main__":
    main()
