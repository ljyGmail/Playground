from bs4 import BeautifulSoup

# Making the soup
with open('index.html') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

soup = BeautifulSoup("<html>a web page</html>", 'html.parser')

print(BeautifulSoup(
    "<html><head></head><body>Sacr&eacute; bleu!</body></html>", "html.parser"))
