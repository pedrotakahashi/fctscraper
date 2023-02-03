import re

import requests
from bs4 import BeautifulSoup

from log import logger


class Scraper:
    """Class responsible for general scraping operations"""

    soup = None

    def __init__(self, *args, **kwargs):
        try:
            self.url = kwargs.pop("url")
            self.scrap_root_url()
        except Exception:
            self.url = ""

    def scrap_root_url(self):
        """Start the BeautifulSoup object of the given url"""
        req = requests.get(self.url, verify=True)
        self.soup = BeautifulSoup(req.content, "html.parser")

    def get_all_hrefs(self):
        """Return all href elements"""
        return self.soup.findAll("a", href=True)

    @staticmethod
    def scrap_url(url):
        """Return the BeautifulSoup object of a given url"""
        children_req = requests.get(url, verify=True)
        return BeautifulSoup(children_req.content, "html.parser")

    def find_all_occurrences_of_str(self, string):
        """Return a list of string with all occurrences of a string"""
        return self.soup.find_all(string=re.compile(string))

    def get_all_tags_with_str(self, tag, string):
        """Return a list of tags of the given tag that contains the
        given string"""
        return self.soup.find_all(tag, string=string)

    def get_all_tags(self, tag):
        return self.soup.find_all(tag)

    def get_all_tags_with_class(self, tag, cls):
        return self.soup.find_all(tag, attrs={"class": cls})

    def get_first_tag_with_class(self, tag, cls):
        return self.soup.find(tag, attrs={"class": cls})

    def get_first_occurrence_str(self, string):
        """Return the first occurrence of the given string"""
        # return self.soup.find(string=re.compile(string))
        return self.soup.find(string=string)

    def getdata(self, url):
        r = requests.get(url, verify=True)
        return r.text

    def get_links(self):
        dict_href_links = {}
        print(self.url)
        print("\n")
        html_data = self.getdata(self.url)
        soup = BeautifulSoup(html_data, "html.parser")
        list_links = []
        website = self.url if self.url.endswith("/") else f"{self.url}/"
        for link in soup.find_all("a", href=True):
            # Append to list if new link contains original link
            if str(link["href"]).startswith((str(self.url))):
                print('ENTROU AQUI')
                list_links.append(link["href"])

            # Include all href that do not start with website link but with "/"
            print(link["href"])
            print('\n')
            if str(link["href"]).startswith("/") and not str(link["href"]).startswith("//"):
                if link["href"] not in dict_href_links:
                    logger.debug(link["href"])
                    dict_href_links[link["href"]] = None
                    link_with_www = website + link["href"][1:]
                    logger.debug(f"adjusted link = {link_with_www}")
                    list_links.append(link_with_www)

        # Convert list of links to dictionary and define keys as the links and the values as "Not-checked"
        dict_links = dict.fromkeys(list_links, "Not-checked")
        return dict_links

    def get_subpage_links(self, links):
        for link in links:
            # If not crawled through this page start crawling and get links
            if links[link] == "Not-checked":
                dict_links_subpages = self.get_links()
                # Change the dictionary value of the link to "Checked"
                links[link] = "Checked"
            else:
                # Create an empty dictionary in case every link is checked
                dict_links_subpages = {}
            # Add new dictionary to old dictionary
            links = {**dict_links_subpages, **links}
        return links

    def get_all_pages_of_website(self):
        # add website WITH slash on end
        website = self.url if self.url.endswith("/") else f"{self.url}/"
        # create dictionary of website
        dict_links = {website: "Not-checked"}
        website_pages_links = []

        counter, counter2 = None, 0
        while counter != 0:
            counter2 += 1
            dict_links2 = self.get_subpage_links(dict_links)
            # Count number of non-values and set counter to 0 if there are no values within the dictionary equal to the string "Not-checked"
            # https://stackoverflow.com/questions/48371856/count-the-number-of-occurrences-of-a-certain-value-in-a-dictionary-in-python
            counter = sum(value == "Not-checked" for value in dict_links2.values())
            # Print some statements
            logger.debug("")
            logger.debug(f"THIS IS LOOP ITERATION NUMBER {counter2}")
            logger.debug(f"LENGTH OF DICTIONARY WITH LINKS = {len(dict_links2)}")
            logger.debug(f"NUMBER OF 'Not-checked' LINKS =  {counter}")
            logger.debug("")
            dict_links = dict_links2
            # Append the links to the list of pages of the website
            website_pages_links += dict_links
        logger.info(f"{len(dict_links2)} pages found.")
        return website_pages_links

    def set_soup(self, soup):
        self.soup = soup

    def get_soup(self):
        return self.soup
