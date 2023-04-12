from bs4 import BeautifulSoup

html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.prettify())

print(f'title: {soup.title}')
print(f'title name: {soup.title.name}')
print(f'title string: {soup.title.string}')
print(f'title parent name: {soup.title.parent.name}')
print(f'p: {soup.p}')
print(f'p class: {soup.p["class"]}')
print(f'a: {soup.a}')
print(f'fint all a: {soup.find_all("a")}')
print(f'id=link3: {soup.find(id="link3")}')

# One common task is extracting all the URLs found within a page's <a> tages.
for link in soup.find_all('a'):
    print(link.get('href'))

# Another common task is extracting all the text from a page.
print(f'text: {soup.get_text()}')
