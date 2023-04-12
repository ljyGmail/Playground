from bs4 import BeautifulSoup

# Tag
soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')
tag = soup.b
print(f'type of tag: {type(tag)}')

# # name
print(f'tag name: {tag.name}')
tag.name = "blockquote"
print(f'tag after change: {tag}')

# # attrs
tag = BeautifulSoup('<b id="boldest">bold</b>', 'html.parser').b
print(f'id of tag: {tag["id"]}')
print(f'tag attrs: {tag.attrs}')

tag['id'] = 'verybold'
tag['another-attribute'] = 1
print(f'tag after change and add an attribute: {tag}')

del tag['id']
del tag['another-attribute']
print(f'tag after deleting attributes: {tag}')

# tag['id'] KeyError: 'id'
print(f'access attr in a safe way: {tag.get("id")}')

# # Multi-valued attribute
css_soup = BeautifulSoup('<p class="body"></p>', 'html.parser')
print(f'body class: {css_soup.p["class"]}')

css_soup = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser')
print(f'body classes: {css_soup.p["class"]}')

# looks like multi-value but actually not, bs4 will leave the attribute alone
id_soup = BeautifulSoup('<p id="my id"></p>', 'html.parser')
print(f'soup id: {id_soup.p["id"]}')

rel_soup = BeautifulSoup(
    '<p>Back to the <a rel="index first">homepage</a></p>')
print(f'rel attr: {rel_soup.a["rel"]}')
rel_soup.a['rel'] = ['index', 'contents']
print(f'after change rel attr: {rel_soup.p}')

no_list_soup = BeautifulSoup(
    '<p class="body strikeout"></p>', 'html.parser', multi_valued_attributes=None)
print(f'force all attrs to be parsed as string: {no_list_soup.p["class"]}')

print(
    f'get a attr that always is a list: {id_soup.p.get_attribute_list("id")}')

# # in XML that are no multi-valued attributes.
xml_soup = BeautifulSoup('<p class="body strikeout"></p>', 'xml')
print(f'xml_souup attr: {xml_soup.p["class"]}')

# # configure this using the multi_valued_attributes argument
class_is_multi = {'*': 'class'}
xml_soup = BeautifulSoup('<p class="body strikeout"></p>',
                         'xml', multi_valued_attributes=class_is_multi)
print(f'configure multi_valued_attributes: {xml_soup.p["class"]}')
