import requests

url = "https://miyashinblog.com/books/sample.html"
response = requests.get(url)
response.encoding = "utf-8"
print(response.text)

from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text,"html.parser")
h1 = soup.find("h1")
print(h1.text)

h2 = soup.find("h2")
print(h2.text)

p = soup.find("p")
print(p.text)