import re
import mechanize
import requests

'''
For search.sunbiz.org

Mechanize Link obj:
    absolute_url – The absolutized link URL 
    url – The link URL 
    base_url – The base URL against which this link is resolved 
    text – The link text
    tag – The link tag name 
    attrs – The tag attributes

TODO: Match regex from user input to the link object's url field. 

TODO: Prep user input to match search.sunbiz.org's format. 

TODO: Make a request to search.sunbiz.org with user input, validate that the
user's input is a registered business entity in Florida.

TODO: Validate that company input is a registered business entity in Florida
and is active. 

TODO: Input validation!!!!

TODO: CLI (Command line interface)
'''

#browser = mechanize.Browser()
# browser.open('http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder=SPECTRUMETRX&searchTerm=SpecTruMetRx%2C%20Inc')
#browser.open('http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder=SPECTRUM&searchTerm=spectrum')
#links = browser.links()

#print('Response: ', links)

# for link in links:
    # print ('Link text field: ', link.text)

# Using requests
searchQuery = input('Search sunbiz.org: ')
link = f'http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder={searchQuery.upper()}&searchTerm={searchQuery}'
html = requests.get(link).text

'''
Use a regex to get all anchor tags on the page (html).
Most of the anchor tags on the html page are the results to searchQuery, with some exceptions.
'''

anchors = re.findall('\<a.*\>.*\/a>', html, re.M) 

print('HTML: ', html)
print('Anchors: ', anchors)
print('html type: ', type(html))
print('Search query: ', searchQuery)
