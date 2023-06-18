from bs4 import BeautifulSoup
import requests


def parsed(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.prettify()
    return article