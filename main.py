import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import simpledialog
from scraper import Scraper
from log import logger
import codecs


URL, KEYWORD = "", ""
root = tk.Tk()
root.withdraw()


def crawl_from_url():
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
            matches += soup.find_all(text=lambda text: KEYWORD in text)
        except Exception as e:
            logger.error(f"Error scraping page: {page_link}")
            logger.error(e)

    # Escreve os textos encontrados em um arquivo .txt
    with codecs.open("resultados.txt", "w", "utf-8") as f:
        for match in matches:
            f.write(match + "\n")

    # Escreve os textos encontrados em uma planilha xls
    with open("resultados.csv", mode="w",newline='', encoding="utf-8") as csv_file:
        fieldnames = ["palavra-chave", "textos"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for match in matches:
            writer.writerow({"palavra-chave": KEYWORD, "textos": match})

def gui():
    global URL, KEYWORD
    # URL do site a ser rastreado
    URL = simpledialog.askstring("palavra Chave", "Insira site", parent=root)

    # Palavra-chave a ser procurada
    KEYWORD = simpledialog.askstring(
        "palavra Chave", "Insira Palavra chave", parent=root
    )


def main():
    gui()
    crawl_from_url()


if __name__ == "__main__":
    main()
