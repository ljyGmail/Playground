from bs4 import BeautifulSoup

with open('result.html') as fp:
    soup = BeautifulSoup(fp, 'lxml')
    rows = soup.find_all('tr', class_='resultB')

    for row in rows:
        td = row.td
        print(td.contents[0].string.text.strip().replace('\n      ', ''))
        print(td.contents[2].string.text)
        print(td.contents[4].string.text)
